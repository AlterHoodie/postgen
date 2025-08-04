import asyncio
import logging
import uuid
from typing import List, Optional, Tuple, Dict
from pathlib import Path
import json
import io

from src.agents import copy_extractor, image_desc_generator, image_generator, html_template_generator, image_query_creator, image_search_agent, image_cropper
from src.mongo_client import get_mongo_client
from src.utils import cleanup_files, capture_html_screenshot, crop_image

logger = logging.getLogger(__name__)

async def generate_single_image( analysis: dict, session_id: str,model:str) -> Tuple[Dict[str, str], List[str]]:
    """Process a single image: generate, save, create HTML, and capture screenshot
    
    Returns:
        Tuple of (image_paths_dict, temp_files_list)
        image_paths_dict contains both 'without_text' and 'with_text' image paths
    """
    
    # Create unique file paths using session_id
    temp_dir = Path("./data/scoopwhoop/temp")
    temp_dir.mkdir(exist_ok=True)
    
    # File paths for both versions
    image_without_text_path = f"./data/scoopwhoop/temp/image_generated_{session_id}_{model}.png"
    html_path = f"./data/scoopwhoop/temp/html_template_{session_id}_generated_{model}.html"
    image_with_text_path = f"./data/scoopwhoop/temp/image_generated_with_text_{session_id}_{model}.png"
    
    temp_files = [html_path, image_without_text_path, image_with_text_path]  # Track temporary files for cleanup (keep both image versions)
    
    try:
        # Generate image from description
        image_descriptions = await image_desc_generator(query=analysis["headline"])
        image_bytes = await image_generator(query=image_descriptions[0],model=model)
        
        if not image_bytes:
            raise Exception("No image bytes generated - likely due to moderation")
        
        with open(image_without_text_path, "wb") as f:
            f.write(image_bytes)
        # Generate HTML template for this image
        html_template = await html_template_generator(
            image=[image_without_text_path], 
            file_path=f"./image_generated_{session_id}_{model}.png",
            analysis=analysis,
            real=True
        )
        # Save HTML template    
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        
        # Capture screenshot of the final post (WITH TEXT)
        capture_html_screenshot(
            file_path=html_path,
            element_selector=".container",
            output=image_with_text_path
        )
        
        # Return both image paths
        image_paths = {
            "without_text": image_without_text_path,
            "with_text": image_with_text_path
        }
        
        return {
            "type":"generated",
            "model": model,
            "description": image_descriptions[0],
            "image_paths": image_paths,
            "temp_files": temp_files
        }
        
    except Exception as e:
        logger.error(f"Error processing generated image {model} {session_id}: {e}")
        return {
            "type":"generated",
            "model": model,
            "description": None,
            "image_paths": {
                "without_text": None,
                "with_text": None
            },
            "temp_files": [],
            "error": str(e)
        }

async def process_single_image(analysis:dict,image_query:str, image_data:dict, session_id:str, index:int) -> Tuple[Dict[str, str], List[str]]:
    """Process a single image: generate, save, create HTML, and capture screenshot
    
    Returns:
        Tuple of (image_paths_dict, temp_files_list)
        image_paths_dict contains both 'without_text' and 'with_text' image paths
    """
    try:
        # File paths for both versions
        image_without_text_path_og = f"./data/scoopwhoop/temp/real_image_{session_id}_{index}_og.png"
        image_without_text_path = f"./data/scoopwhoop/temp/real_image_{session_id}_{index}.png"
        html_path = f"./data/scoopwhoop/temp/html_template_{session_id}_{index}_real.html"
        image_with_text_path = f"./data/scoopwhoop/temp/image_real_with_text_{session_id}_{index}.png"

        temp_files = [html_path, image_without_text_path, image_with_text_path,image_without_text_path_og]  # Track temporary files for cleanup (keep both image versions)

        image_bytes_og = image_data['image_data'].getvalue()

        with open(image_without_text_path_og, "wb") as f:
            f.write(image_bytes_og)

        cropped_image_bytes = crop_image(image_bytes_og,bias=0.5)
        bias = await image_cropper(cropped_image_bytes,headline=analysis["headline"])
        cropped_image_bytes = crop_image(image_bytes_og,bias=bias['bias'])
        # Save generated image (WITHOUT TEXT)
        with open(image_without_text_path, "wb") as f:
            f.write(cropped_image_bytes)

        # Generate HTML template for this image
        html_template = await html_template_generator(
            image=[image_without_text_path], 
            file_path=f"./real_image_{session_id}_{index}.png",
            analysis=analysis,
            real=True
        )

        # Save HTML template
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_template)

        # Capture screenshot of the final post (WITH TEXT)
        capture_html_screenshot(
            file_path=html_path,
            element_selector=".container",
            output=image_with_text_path
        )

        # Return both image paths
        image_paths = {
            "without_text": image_without_text_path,
            "with_text": image_with_text_path
        }

        return {
            "type":"real",
            "model":f"Reasoning: {image_data['reasoning']}\nScore: {image_data['score']}",
            "description": image_query,
            "image_paths": image_paths,
            "temp_files": temp_files
        }
    except Exception as e:
        logger.error(f"Error processing real image {session_id}: {e}")
        return {
            "type":"real",
            "model":None,
            "description": image_query,
            "image_paths": {
                "without_text": None,
                "with_text": None
            },
            "temp_files": [],
            "error": str(e)
        }

async def fetch_multiple_images(analysis: dict, session_id: str, reference_image:bytes = None) -> Tuple[Dict[str, str], List[str]]:
    """Process a single image: generate, save, create HTML, and capture screenshot
    
    Returns:
        Tuple of (image_paths_dict, temp_files_list)
        image_paths_dict contains both 'without_text' and 'with_text' image paths
    """
    
    # Create unique file paths using session_id
    temp_dir = Path("./data/scoopwhoop/temp")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        image_query = await image_query_creator(headline=analysis["headline"], image=reference_image)
        image_query_json = json.loads(image_query)

        # Generate image from description
        image_bytes_list = await image_search_agent(query=image_query_json["queries"][0], reference_image=reference_image)

        processed_tasks = await asyncio.gather(*[process_single_image(analysis, image_query_json["queries"][0], image_data, session_id, index) for index, image_data in enumerate(image_bytes_list)])
        
        return processed_tasks
        
    except Exception as e:
        logger.error(f"Error processing real image {session_id}: {e}")
        return []

async def workflow(image_bytes: bytes, store_in_db: bool = True) -> Optional[str]:
    """
    Run the complete workflow and optionally store results in MongoDB
    
    Args:
        image_bytes: Reference image bytes for analysis
        store_in_db: Whether to store results in MongoDB
        
    Returns:
        document_id if stored in DB, None otherwise
    """
    # Generate unique session ID for this workflow run
    session_id = str(uuid.uuid4())[:8]  # Use first 8 characters of UUID
    logger.info(f"Starting workflow with session ID: {session_id}")
    
    analyze_path = f"./data/scoopwhoop/temp/analyze_{session_id}.png"
    all_temp_files = []
    all_image_results = []
    document_id = None
    try:
        # Save reference image for analysis
        with open(analyze_path, "wb") as f:    
            f.write(image_bytes)
        all_temp_files.append(analyze_path)
        
        # Extract copy from the reference image
        analysis = await copy_extractor(image=[analyze_path])
        logger.info(f"Extracted analysis: {analysis}")

        tasks = [
            fetch_multiple_images( analysis, session_id, image_bytes),
            # generate_single_image( analysis, f"{session_id}_0",model="gpt-image-1"),
            # generate_single_image( analysis, f"{session_id}_1",model="gpt-image-1"),
            # generate_single_image( analysis, f"{session_id}_2",model="gpt-image-1"),
            # generate_single_image( analysis, f"{session_id}_0",model="imagen-4.0-ultra-generate-preview-06-06"),
            # generate_single_image( analysis, f"{session_id}_1",model="imagen-4.0-ultra-generate-preview-06-06"),
            # generate_single_image( analysis, f"{session_id}_2",model="imagen-4.0-ultra-generate-preview-06-06"),
        ]
        
        # Wait for all images to be processed in parallel
        results = await asyncio.gather(*tasks)
        
        all_results = results[0]
        all_results.extend(results[1:])
        # Collect all results and temporary files
        for result in all_results:
            all_image_results.append({
                "type": result["type"],
                "model": result["model"],
                "description": result["description"],
                "paths": result["image_paths"],
                "error": result.get("error", None)
            })
            all_temp_files.extend(result["temp_files"])
        
        logger.info(f"Generated {len(all_image_results)} image sets (with and without text)")
        
        # Store in MongoDB if requested
        if store_in_db:
            try:
                mongo_client = get_mongo_client()
                document_id = mongo_client.store_workflow_result(
                    session_id=session_id,
                    analysis=analysis,
                    image_results=all_image_results
                )
                mongo_client.close()
                logger.info(f"Stored workflow results in MongoDB with document_id: {document_id}")
            except Exception as e:
                logger.error(f"Failed to store in MongoDB: {e}")
        return session_id
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        raise
    finally:
        # Clean up temporary files (HTML templates and reference image)
        cleanup_files(all_temp_files)
        logger.info(f"Finished Workflow with session ID: {session_id}")

if __name__ == "__main__":
    with open("./data_/image_12.png", "rb") as f:
        image_bytes = f.read()
    print(asyncio.run(workflow(image_bytes, store_in_db=True)))