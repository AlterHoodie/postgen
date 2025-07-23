import json
import string
import asyncio
import logging
import uuid
import os
from pathlib import Path
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

def cleanup_files(file_paths: List[str]) -> None:
    """Delete all temporary files generated during the workflow"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                if "logo.png" in file_path:
                    continue
                os.remove(file_path)
                logger.info(f"Deleted temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to delete file {file_path}: {e}")

async def process_single_image(description: str, index: int, analysis: dict, session_id: str) -> Tuple[str, List[str]]:
    """Process a single image: generate, save, create HTML, and capture screenshot"""
    
    # Create unique file paths using session_id
    temp_dir = Path("./data/scoopwhoop/temp")
    temp_dir.mkdir(exist_ok=True)
    
    image_path = f"./data/scoopwhoop/temp/generated_image_{session_id}_{index}.png"
    html_path = f"./data/scoopwhoop/temp/html_template_{session_id}_{index}.html"
    output_path = f"./data/scoopwhoop/temp/generated_image_with_text_{session_id}_{index}.png"
    
    temp_files = [image_path, html_path]  # Track temporary files for cleanup
    
    try:
        # Generate image from description
        image_bytes = await image_generator(query=description)
        
        # Save generated image
        with open(image_path, "wb") as f:
            f.write(image_bytes)
        logger.info(f"Saved generated image: {image_path}")
        
        # Generate HTML template for this image
        html_template = await html_template_generator(
            image=[image_path], 
            file_path=f"./generated_image_{session_id}_{index}.png",
            analysis=analysis
        )
        
        # Save HTML template
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        logger.info(f"Saved HTML template: {html_path}")
        
        # Capture screenshot of the final post
        capture_html_screenshot(
            file_path=html_path,
            element_selector=".container",
            output=output_path
        )
        logger.info(f"Saved final post image: {output_path}")
        
        return output_path, temp_files
        
    except Exception as e:
        logger.error(f"Error processing image {index}: {e}")
        raise

async def test_workflow() -> List[str]:
    # Generate unique session ID for this workflow run
    session_id = str(uuid.uuid4())[:8]  # Use first 8 characters of UUID
    logger.info(f"Starting workflow with session ID: {session_id}")
    
    all_temp_files = []
    final_outputs = []
    
    try:
        # Extract copy from the reference image
        analysis = await copy_extractor(image=["./data/scoopwhoop/analyze.png"])
        
        # Generate 3 image descriptions
        image_descriptions = await image_desc_generator(query=analysis["headline"])
        logger.info(f"Generated {len(image_descriptions)} image descriptions")
        
        # Process all 3 images in parallel
        logger.info("Starting parallel image generation...")
        tasks = [
            process_single_image(description, i+1, analysis, session_id) 
            for i, description in enumerate(image_descriptions)
        ]
        
        # Wait for all images to be processed in parallel
        results = await asyncio.gather(*tasks)
        
        # Separate final outputs and temporary files
        for output_path, temp_files in results:
            final_outputs.append(output_path)
            all_temp_files.extend(temp_files)
        
        logger.info("Successfully generated 3 complete social media posts in parallel!")
        logger.info(f"Final output files: {final_outputs}")
        
        return final_outputs
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        raise
    finally:
        # Clean up all temporary files
        logger.info("Cleaning up temporary files...")
        cleanup_files(all_temp_files)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_workflow())