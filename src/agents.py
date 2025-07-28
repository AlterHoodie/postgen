import json
import logging
from typing import List
import os
import io
import asyncio

from serpapi import GoogleSearch

from src.prompts import IMAGE_DESCRIPTION_PROMPT, COPY_EXTRACTOR_PROMPT, TEMPLATE_PROMPT, HTML_TEMPLATE_PROMPT, IMAGE_QUERY_PROMPT, IMAGE_SCORER_PROMPT, HTML_TEMPLATE_PROMPT_REAL
from src.utils import extract_x
from src.clients import openai_response, openai_image_response, download_image

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

async def html_template_generator(image:List[str] = [],file_path:str = "", analysis:dict = {}, real:bool = False) -> str:
    prompt = TEMPLATE_PROMPT.format(analysis)
    response = await openai_response(prompt=prompt, images=image, model = "gpt-4.1")
    input_json = json.loads(extract_x(response,"json"))
    if real:
        html_template = HTML_TEMPLATE_PROMPT_REAL.format(**input_json, file_path=file_path)
    else:
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


async def image_scorer_agent(images:List[io.BytesIO],query:str)->List[dict]:
    prompt = IMAGE_SCORER_PROMPT.format(query)
    response = await openai_response(prompt,images=images,model="gpt-4.1",type="bytes")
    return extract_x(response,'json')

async def image_query_creator(headline:str)->dict:
    prompt = IMAGE_QUERY_PROMPT.format(headline)
    response = await openai_response(prompt,model="gpt-4.1", tools=[{"type":"web_search_preview"}],type="bytes")
    return extract_x(response,'json')

async def image_search_agent(query: str) -> dict:
    """
    Image search agent that finds and selects the best image for a given query.
    
    This function implements a multi-stage image selection process:
    1. Uses SERP API to search for images related to the query
    2. Downloads up to 20 images and validates they are actual images
    3. Uses AI to score each image based on quality and relevance
    4. Filters out low-quality images (score < 6)
    5. Selects top 5 images based on scores
    6. Uses AI to select the single best image from the top 5
    
    Args:
        query (str): The search query to find relevant images
        
    Returns:
        dict: Selected image with metadata including:
            - image_url: Direct image URL
            - image_description: Image title/description
            - image_source: Source website
            - image_cite: Citation link
            - image_data: BytesIO object with image data
            - score: AI-assigned quality score (0-10)
        None: If no suitable images are found
        
    Example:
        >>> image = await image_search_agent("Ramayana movie poster")
        >>> print(f"Selected: {image['image_description']} (Score: {image['score']})")
    """
    try:
        # Step 1: Search for images using SERP API
        params = {
            "engine": "google_images",
            "q": query,
            "gl": "in",
            "api_key": os.getenv("SERP_API_KEY"),
            "imgsz": "svga"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "error" in results:
            logging.error(f"SERP API error: {results['error']}")
            return []
        
        # Extract image data (top 5)
        images_data = []
        for img in results.get('images_results', []):
            images_data.append({
                "image_url": img.get('original', ''),
                "image_description": img.get('title', ''),
                "image_source": img.get('source', ''),
                "image_cite": img.get('link', '')
            })
        
        if not images_data:
            logging.warning("No images found from SERP API")
            return []
        
        logging.info(f"Found {len(images_data)} images, downloading...")
        
        # Step 2: Download images to memory
        downloaded_images = []
        for i, img_data in enumerate(images_data):
            image_data = await download_image(img_data['image_url'])
            if image_data:
                downloaded_images.append({
                    **img_data,
                    "image_data": image_data
                })
                logging.info(f"Downloaded image {i+1}: {img_data['image_description']}")
            else:
                logging.warning(f"Failed to download image {i+1}")
            
            if len(downloaded_images) == 20:
                break
        
        # Step 3: Score all downloaded images using AI concurrently
        if downloaded_images:
            logging.info(f"Scoring {len(downloaded_images)} images concurrently...")
            
            try:
                # Create individual scoring tasks for each image
                scoring_tasks = []
                for img_data in downloaded_images:
                    # Send single image to scorer
                    task = image_scorer_agent([img_data['image_data']], query)
                    scoring_tasks.append((img_data, task))
                
                # Execute all scoring tasks concurrently using asyncio.gather
                scoring_responses = await asyncio.gather(
                    *[task for _, task in scoring_tasks], 
                    return_exceptions=True
                )
                
                # Process results and assign scores
                for i, ((img_data, _), response) in enumerate(zip(scoring_tasks, scoring_responses)):
                    if isinstance(response, Exception):
                        logging.error(f"Failed to score image {i+1}: {response}")
                        img_data['score'] = 5  # Default score
                    else:
                        try:
                            scoring_result = json.loads(response)
                            score = scoring_result.get('image_score', [])
                            if score:
                                img_data['score'] = score  # Single image, first score
                            else:
                                img_data['score'] = 0.5  # Default score
                        except Exception as e:
                            logging.error(f"Failed to parse score for image {i+1}: {e}")
                            img_data['score'] = 0.1  # Default score
                
                logging.info(f"Successfully scored {len(downloaded_images)} images concurrently")
                
            except Exception as e:
                logging.error(f"Failed to score images: {e}")
                # Assign default scores if scoring fails
                for img_data in downloaded_images:
                    img_data['score'] = 0.5  # Default score
        
        # Step 4: Filter out low-quality images (score < 6)
        filtered_images = [img for img in downloaded_images if img.get('score', 0) >= 0.6]
        logging.info(f"Filtered images: {len(filtered_images)}")
        if not filtered_images:
            logging.warning("No images passed quality threshold (score >= 0.6), using all images")
            filtered_images = downloaded_images
        
        # Step 5: Select top 5 images based on score
        top_image = sorted(filtered_images, key=lambda x: x.get('score', 0), reverse=True)[0]

        if not top_image:
            logging.error("No images could be processed")
            return None 
        
        return top_image
    except Exception as e:
        logging.error(f"Error in image search agent: {e}")
        return None

async def test_workflow(headline:str):
    image_query = await image_query_creator(headline)
    image_search = await image_search_agent(image_query)
    return image_search

if __name__ == "__main__":
    import asyncio
    image = asyncio.run(test_workflow("Ka Ka Menon starrer Special Ops 2  shines as fans appreciate • acting, storyline and thrill"))
    with open("./data_/image.png", "wb") as f:
        f.write(image["image_data"].getvalue())