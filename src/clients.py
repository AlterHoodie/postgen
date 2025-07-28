from typing import List, Tuple
import base64
import os 
from dotenv import load_dotenv
import logging
import io

import httpx
import openai
import anthropic

load_dotenv(override=True)
logging.basicConfig(level=logging.INFO)

openai_client = openai.AsyncClient(api_key=os.getenv("OPENAI_API_KEY"))
# anthropic_client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


async def openai_response(
    prompt, model: str = "gpt-4.1", use_web_search: bool = False, tools: List[str] = [], images: List[str] = [], type:str = "path"
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
                encoded_image = base64.standard_b64encode(image.getvalue() if isinstance(image, io.BytesIO) else image).decode("utf-8") if image else ""
                messages.append(
                    {
                        "type": "input_image",
                        "image_url": f"data:{media_type};base64,{encoded_image}",
                    }
                )

    messages.append({"type": "input_text", "text": prompt})
    if use_web_search:
        response = await openai_client.responses.create(
            model=model, input=[{"role": "user", "content": messages}],
            tools=[{"type": "web_search_preview", "search_context_size": "low"}] + tools
        )
        return response.output_text
    else:
        response = await openai_client.responses.create(
            model=model, input=[{"role": "user", "content": messages}],
            tools=tools
        )

    return response.output_text

async def openai_image_response(prompt:str, images:List[str] = [],timeout=200):
    if images:
        result = await openai_client.images.edit(
        model="gpt-image-1",
        prompt=prompt,
        image=[open(image, "rb") for image in images],
        size = "1024x1536",
        quality="high",
        timeout=timeout
        )
    else:
        result = await openai_client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size = "1024x1536",
            quality="high",
            timeout=timeout
        )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return image_bytes

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
            content_type = response.headers.get('content-type', '').lower()
            if not content_type.startswith('image/'):
                logging.warning(f"URL does not return an image content type: {content_type} for {image_url}")
                return None
            
            # Create BytesIO object with image data
            image_data = io.BytesIO(response.content)
            image_data.name = "image.jpg"  # Default name
            
            logging.info(f"Downloaded image: {image_url}")
            return image_data
    except Exception as e:
        logging.error(f"Failed to download image {image_url}: {e}")
        return None

# async def anthropic_response(images: List[str], prompt:str, model:str) -> Tuple[dict, dict]:
#     messages = []

#     for image in images:
#         with open(image, "rb") as f:
#             encoded_image = base64.b64encode(f.read()).decode("utf-8")
#         messages.append(
#             {
#                 "type": "image",
#                 "source": {
#                     "type": "base64",
#                     "media_type": "image/png",
#                     "data": encoded_image,
#                 },
#             }
#         )
#     messages.append({"type": "text", "text": prompt})

#     response = await anthropic_client.messages.create(
#         model=model,
#         max_tokens=2000,
#         messages=[{"role": "user", "content": messages}],
#     )
    
#     return response.content[0].text