import asyncio
import logging
import uuid
from typing import List, Optional, Tuple, Dict
from pathlib import Path

from src.agents import copy_extractor, image_desc_generator, image_generator, html_template_generator
from src.mongo_client import get_mongo_client
from src.utils import cleanup_files, capture_html_screenshot,compress_image

logger = logging.getLogger(__name__)

async def process_single_image(description: str, index: int, analysis: dict, session_id: str) -> Tuple[Dict[str, str], List[str]]:
    """Process a single image: generate, save, create HTML, and capture screenshot
    
    Returns:
        Tuple of (image_paths_dict, temp_files_list)
        image_paths_dict contains both 'without_text' and 'with_text' image paths
    """
    
    # Create unique file paths using session_id
    temp_dir = Path("./data/scoopwhoop/temp")
    temp_dir.mkdir(exist_ok=True)
    
    # File paths for both versions
    image_without_text_path = f"./data/scoopwhoop/temp/generated_image_{session_id}_{index}.png"
    html_path = f"./data/scoopwhoop/temp/html_template_{session_id}_{index}.html"
    image_with_text_path = f"./data/scoopwhoop/temp/generated_image_with_text_{session_id}_{index}.png"
    
    temp_files = [html_path, image_without_text_path, image_with_text_path]  # Track temporary files for cleanup (keep both image versions)
    
    try:
        # Generate image from description
        image_bytes = await image_generator(query=description)
        
        # Save generated image (WITHOUT TEXT)
        with open(image_without_text_path, "wb") as f:
            f.write(image_bytes)
        logger.info(f"Saved generated image (without text): {image_without_text_path}")
        
        # Generate HTML template for this image
        html_template = await html_template_generator(
            image=[image_without_text_path], 
            file_path=f"./generated_image_{session_id}_{index}.png",
            analysis=analysis
        )
        
        # Save HTML template
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        logger.info(f"Saved HTML template: {html_path}")
        
        # Capture screenshot of the final post (WITH TEXT)
        capture_html_screenshot(
            file_path=html_path,
            element_selector=".container",
            output=image_with_text_path
        )
        logger.info(f"Saved final post image (with text): {image_with_text_path}")
        
        # Return both image paths
        image_paths = {
            "without_text": image_without_text_path,
            "with_text": image_with_text_path
        }
        
        return image_paths, temp_files
        
    except Exception as e:
        logger.error(f"Error processing image {index}: {e}")
        raise

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
        
        # Collect all results and temporary files
        for image_paths_dict, temp_files in results:
            all_image_results.append({
                "index": len(all_image_results) + 1,
                "description": image_descriptions[len(all_image_results)],
                "paths": image_paths_dict
            })
            all_temp_files.extend(temp_files)
        
        logger.info("Successfully generated 3 complete social media posts in parallel!")
        logger.info(f"Generated {len(all_image_results)} image sets (with and without text)")
        
        # Store in MongoDB if requested
        if store_in_db:
            try:
                mongo_client = get_mongo_client()
                document_id = mongo_client.store_workflow_result(
                    session_id=session_id,
                    analysis=analysis,
                    image_descriptions=image_descriptions,
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
        logger.info("Cleaning up temporary files...")
        # cleanup_files(all_temp_files)

if __name__ == "__main__":
    with open("./data/scoopwhoop/analyze.png", "rb") as f:
        image_bytes = f.read()
    print(asyncio.run(workflow(image_bytes, store_in_db=True)))