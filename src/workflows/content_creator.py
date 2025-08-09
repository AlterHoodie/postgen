import logging
from typing import List, Dict
import uuid

from src.agents import story_board_generator
from src.workflows.editors import image_editor
from src.services.mongo_client import get_mongo_client

logger = logging.getLogger(__name__)

async def story_board_creator(headline: str, template: str) -> Dict:  
    """Generate story board from headline and template"""
    try:
        story_board = await story_board_generator(headline=headline, template=template)
        logger.info(f"Story board created with {len(story_board.get('storyboard', []))} slides")
        return story_board
    except Exception as e:
        logger.error(f"Failed to generate story board: {e}")
        raise

async def slide_creator(slide_template: dict, html_template: dict) -> List[Dict]:
    """Create slides with images and handle errors gracefully"""
    try:
        session_id = str(uuid.uuid4())[:8]
        
        # Generate images from different sources
        # image_tasks = [
        #     fetch_multiple_images(
        #         headline=slide_template['image_description'], 
        #         reference_image=None, 
        #         session_id=session_id
        #     ),
        #     generate_single_image(
        #         headline=slide_template['image_description'], 
        #         session_id=session_id,
        #         model="gpt-image-1"
        #     ),
        #     generate_single_image(
        #         headline=slide_template['image_description'], 
        #         session_id=session_id,
        #         model="imagen-4.0-ultra-generate-preview-06-06"
        #     ),
        # ]

        # results = await asyncio.gather(*image_tasks, return_exceptions=True)
        
        # # Process results and handle individual failures
        # all_images = []
        
        # # Process real images (from fetch_multiple_images)
        # if not isinstance(results[0], Exception) and results[0]:
        #     for img in results[0]:
        #         img['type'] = 'real'
        #         all_images.append(img)
        
        # # Process generated images
        # for i, result in enumerate(results[1:], 1):
        #     if not isinstance(result, Exception) and result:
        #         if isinstance(result, list):
        #             for img in result:
        #                 img['type'] = 'generated'
        #                 all_images.append(img)
        #         else:
        #             result['type'] = 'generated'
        #             all_images.append(result)

        all_images = []
        with open("./data_/test.png", "rb") as f:
            all_images = [{"image_bytes": f.read(), "type": "real"}]
        
        # If no images were generated, return empty list
        if not all_images:
            logger.warning(f"No images generated for slide: {slide_template.get('name', 'unknown')}")
            return []
        
        # Process images with editor
        processed_images = []
        for img_data in all_images:
            try:
                image_bytes = image_editor(
                    image_bytes=img_data['image_bytes'], 
                    text_template=slide_template['text_template'], 
                    html_template=html_template[slide_template['name']]
                )
                processed_images.append({
                    'image_bytes': image_bytes,
                    'type': img_data['type'],
                    'model': img_data.get('model', 'unknown')
                })
            except Exception as e:
                logger.warning(f"Failed to process image: {e}")
                continue

        return processed_images
        
    except Exception as e:
        logger.error(f"Error in slide_creator: {e}")
        return []

async def save_to_mongo(session_id: str, headline: str, template_type: str, 
                       story_board: dict, slide_images: list, error: str = None) -> str:
    """Helper function to save workflow results to MongoDB"""
    try:
        mongo_client = get_mongo_client()
        document_id = mongo_client.store_content_workflow(
            session_id=session_id,
            headline=headline,
            template_type=template_type,
            story_board=story_board,
            slide_images=slide_images,
            error=error
        )
        mongo_client.close()
        logger.info(f"Saved to MongoDB. Document ID: {document_id}")
        return document_id
    except Exception as e:
        logger.error(f"MongoDB save failed: {e}")
        raise

async def workflow(headline: str, template: dict, save: bool = True) -> str:
    """Main workflow function that creates content and optionally saves to MongoDB"""
    session_id = str(uuid.uuid4())[:8]
    
    try:
        # Generate story board
        story_board = await story_board_creator(
            headline=headline, 
            template=template['text_template']
        )
        
        # Generate slides with images
        slide_results = []
        for slide in story_board.get('storyboard', []):
            slide_images = await slide_creator(
                slide_template=slide,
                html_template=template['html_template']
            )
            slide_results.append(slide_images)
        
        # Save to MongoDB if requested
        if save:
            document_id = await save_to_mongo(
                session_id=session_id,
                headline=headline,
                template_type=template['template_type'],
                story_board=story_board,
                slide_images=slide_results,
                error=None
            )
        
        logger.info(f"Workflow completed successfully. Session: {session_id}")
        return session_id
        
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        
        # Save error state to MongoDB if requested
        if save:
            try:
                document_id = await save_to_mongo(
                    session_id=session_id,
                    headline=headline,
                    template_type=template.get('template_type', 'unknown'),
                    story_board={},
                    slide_images=[],
                    error=str(e)
                )
            except Exception as mongo_error:
                logger.error(f"Failed to save error state to MongoDB: {mongo_error}")
        
        return session_id


if __name__ == "__main__":
    import asyncio
    import base64
    from src.templates.thumbnail import (
        TEXT_TEMPLATE, HEADLINE_SLIDE_HTML_TEMPLATE
    )
    
    template = {
        "template_type": "thumbnail",
        "text_template": TEXT_TEMPLATE,
        "html_template": {
            "headline_slide": HEADLINE_SLIDE_HTML_TEMPLATE,
        }
    }

    headline = "UttarKashi Cloud Burst India"
    
    try:
        session_id = asyncio.run(workflow(headline=headline, template=template))
        # session_id = "45c92cdd"
        print(f"Workflow completed successfully!")
        print(f"Document ID: {session_id}")
        mongo_client = get_mongo_client()
        result = mongo_client.get_workflow_result(session_id)
        for slide in result['slides']:
            for img in slide['images']:
                b64_img = base64.b64decode(img['image_base64'])
                with open(f"./data_/slide_1/test_{slide['slide_index']}.png", "wb") as f:
                    f.write(b64_img)
        mongo_client.close()
    except Exception as e:
        print(f"Workflow failed: {e}")