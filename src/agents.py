import json
import string
import asyncio
import logging
from typing import List, Tuple

from src.prompts import IMAGE_DESCRIPTION_PROMPT, COPY_EXTRACTOR_PROMPT, TEMPLATE_PROMPT, HTML_TEMPLATE_PROMPT
from src.utils import extract_x, capture_html_screenshot
from src.clients import openai_response, openai_image_response

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

async def copy_extractor(image:List[str] = []) -> str:
    prompt = COPY_EXTRACTOR_PROMPT
    response = await openai_response(prompt=prompt, images=image, model = "gpt-4.1")
    return json.loads(extract_x(response,"json"))

async def html_template_generator(image:List[str] = [],file_path:str = "", analysis:dict = {}) -> str:
    prompt = TEMPLATE_PROMPT.format(analysis)
    response = await openai_response(prompt=prompt, images=image, model = "gpt-4.1")
    input_json = json.loads(extract_x(response,"json"))
    html_template = HTML_TEMPLATE_PROMPT.format(**input_json, file_path=file_path)
    return html_template

async def image_desc_generator(query:str = "") -> List[str]:
    prompt = IMAGE_DESCRIPTION_PROMPT.format(query)
    response = await openai_response(prompt=prompt, model = "gpt-4.1")
    parsed_response = json.loads(extract_x(response, "json"))
    return parsed_response["image_description"]

async def image_generator(query:str = "") -> bytes:
    response = await openai_image_response(prompt=query)
    return response

async def process_single_image(description: str, index: int, analysis: dict) -> str:
    """Process a single image: generate, save, create HTML, and capture screenshot"""
    
    # Generate image from description
    image_bytes = await image_generator(query=description)
    
    # Save generated image
    image_path = f"./data/scoopwhoop/generated_image_{index}.png"
    with open(image_path, "wb") as f:
        f.write(image_bytes)
    logger.info(f"Saved generated image: {image_path}")
    
    # Generate HTML template for this image
    html_template = await html_template_generator(image=[image_path], file_path=f"./generated_image_{index}.png",analysis=analysis)
    
    # Save HTML template
    html_path = f"./data/scoopwhoop/html_template_{index}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_template)
    logger.info(f"Saved HTML template: {html_path}")
    
    # Capture screenshot of the final post
    output_path = f"./data/scoopwhoop/generated_image_with_text_{index}.png"
    capture_html_screenshot(
        file_path=html_path,
        element_selector=".container",
        output=output_path
    )
    logger.info(f"Saved final post image: {output_path}")
    
    return output_path

async def test_workflow() -> None:
    # Extract copy from the reference image
    analysis = await copy_extractor(image=["./data/scoopwhoop/analyze.png"])
    
    # Generate 3 image descriptions
    image_descriptions = await image_desc_generator(query=analysis["headline"])
    logger.info(f"Generated {len(image_descriptions)} image descriptions")
    
    # Process all 3 images in parallel
    logger.info("Starting parallel image generation...")
    tasks = [
        process_single_image(description, i+1, analysis) 
        for i, description in enumerate(image_descriptions)
    ]
    
    # Wait for all images to be processed in parallel
    results = await asyncio.gather(*tasks)
    
    logger.info("Successfully generated 3 complete social media posts in parallel!")
    logger.info(f"Generated files: {results}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_workflow())