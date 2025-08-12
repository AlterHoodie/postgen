from typing import List, Tuple
import base64
import os
from dotenv import load_dotenv
import logging
import io
import asyncio

import httpx
import openai
from google import genai
from google.genai import types

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO)

openai_client = openai.AsyncClient(api_key=os.getenv("OPENAI_API_KEY"), timeout=150)
google_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def sync_download_image(image_url: str) -> io.BytesIO:
    """
    Download image from URL and return as BytesIO object
    Returns the image data as BytesIO object if it's a valid image
    """
    try:
        with httpx.Client() as client:
            response = client.get(image_url, timeout=10)
            response.raise_for_status()

            # Check if content type is an image
            content_type = response.headers.get("content-type", "").lower()
            if not content_type.startswith("image/"):
                logging.warning(
                    f"URL does not return an image content type: {content_type} for {image_url}"
                )
                return None

            # Create BytesIO object with image data
            image_data = io.BytesIO(response.content)
            image_data.name = "image.jpg"  # Default name
            return image_data
    except Exception as e:
        logging.error(f"Failed to download image {image_url}: {e}")
        return None


async def download_image(image_url: str) -> io.BytesIO:
    """
    Download image from URL and return as BytesIO object
    Returns the image data as BytesIO object if it's a valid image
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(image_url, timeout=10)
            response.raise_for_status()

            # Check if content type is an image
            content_type = response.headers.get("content-type", "").lower()
            if not content_type.startswith("image/"):
                logging.warning(
                    f"URL does not return an image content type: {content_type} for {image_url}"
                )
                return None

            # Create BytesIO object with image data
            image_data = io.BytesIO(response.content)
            image_data.name = "image.jpg"  # Default name
            return image_data
    except Exception as e:
        logging.error(f"Failed to download image {image_url}: {e}")
        return None


async def openai_response(
    prompt,
    model: str = "gpt-4.1",
    use_web_search: bool = False,
    tools: List[str] = [],
    images: List[str] = [],
    type: str = "path",
) -> Tuple[dict, dict]:

    media_type = "image/png"
    messages = []
    if type == "path":
        for image in images:
            with open(image, "rb") as f:
                encoded_image = base64.standard_b64encode(f.read()).decode("utf-8")

            messages.append(
                {
                    "type": "input_image",
                    "image_url": f"data:{media_type};base64,{encoded_image}",
                }
            )
    else:
        for image in images:
            if image:
                encoded_image = (
                    base64.standard_b64encode(
                        image.getvalue() if isinstance(image, io.BytesIO) else image
                    ).decode("utf-8")
                    if image
                    else ""
                )
                messages.append(
                    {
                        "type": "input_image",
                        "image_url": f"data:{media_type};base64,{encoded_image}",
                    }
                )

    messages.append({"type": "input_text", "text": prompt})
    if use_web_search:
        response = await openai_client.responses.create(
            model=model,
            input=[{"role": "user", "content": messages}],
            tools=[{"type": "web_search_preview", "search_context_size": "low"}]
            + tools,
            timeout=150,
        )
        return response.output_text
    else:
        response = await openai_client.responses.create(
            model=model, input=[{"role": "user", "content": messages}], tools=tools
        )

    return response.output_text


async def openai_image_response(
    prompt: str, images: List[str] = [], timeout=150, model="gpt-image-1"
) -> bytes:

    if model == "dall-e-3":
        size = "1024x1024"
        quality = "hd"

        result = await openai_client.images.generate(
            model=model, prompt=prompt, size=size, quality=quality, timeout=timeout
        )
        url = result.data[0].url
        image_bytes = await download_image(url)

        return image_bytes.getvalue()
    else:
        size = "1024x1536"
        quality = "high"

        if images:
            result = await openai_client.images.edit(
                model=model,
                prompt=prompt,
                image=[open(image, "rb") for image in images],
                size=size,
                quality=quality,
                timeout=timeout,
            )
        else:
            result = await openai_client.images.generate(
                model=model, prompt=prompt, size=size, quality=quality, timeout=timeout
            )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        return image_bytes


async def google_image_response(
    prompt: str, timeout=100, model="imagen-4.0-ultra-generate-preview-06-06"
) -> bytes:
    response = await asyncio.wait_for(
        google_client.aio.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            ),
        ),
        timeout=timeout,
    )
    # Get the image (assuming it's a PIL Image object)
    if response.generated_images:
        image = response.generated_images[0].image
        return image.image_bytes
    else:
        return None


async def flux_image_response(
    prompt: str, timeout=200, model="flux-pro-1.1-ultra"
) -> bytes:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.bfl.ai/v1/{model}",
            headers={
                "accept": "application/json",
                "x-key": os.environ.get("FLUX_API_KEY"),
                "Content-Type": "application/json",
            },
            json={"prompt": prompt, "aspect_ratio": "3:4"},
            timeout=timeout,
        )
        request = response.json()

        request_id = request["id"]
        polling_url = request["polling_url"]
        while True:
            await asyncio.sleep(1)
            response = await client.get(
                polling_url,
                headers={
                    "accept": "application/json",
                    "x-key": os.getenv("FLUX_API_KEY"),
                },
                params={
                    "id": request_id,
                },
                timeout=timeout,
            )
            result = response.json()

            status = result["status"]

            if status == "Ready":
                signed_url = result["result"]["sample"]
                break
            elif status in ["Error", "Failed"]:
                logging.error(f"Generation failed: {result}")
                raise Exception(f"Flux Generation failed: {result}")

    image_bytes = await download_image(signed_url)
    return image_bytes.getvalue()


if __name__ == "__main__":
    image_bytes = asyncio.run(
        google_image_response(
            "A cat on its back legs running like a human is holding a big silver fish with its arms. The cat is running away from the shop owner and has a panicked look on his face. The scene is situated in a crowded market."
        )
    )
    with open("./data_/google_image.png", "wb") as f:
        f.write(image_bytes)
