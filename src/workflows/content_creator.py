import logging
from typing import List, Dict
import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor

from src.agents import story_board_generator, content_research_agent
from src.workflows.editors import text_editor
from src.services.mongo_client import get_mongo_client
from src.workflows.image_gen import fetch_multiple_images, generate_single_image

logger = logging.getLogger(__name__)


async def story_board_creator(headline: str, text_template: str,image_bytes: bytes) -> Dict:
    """Generate story board from headline and template"""
    try:
        # Research the headline
        research_result = await content_research_agent(
            headline=headline, 
            template=text_template['template_description']
        )

        # Generate story board with research context
        template_context = f"{text_template['template_description']}\n{text_template['json_description']}"
        story_board = await story_board_generator(
            headline=headline,
            research_result=research_result, 
            template=template_context,
            image_bytes=image_bytes
        )

        slide_count = len(story_board.get('storyboard', []))
        logger.info(f"Story board created with {slide_count} slides")
        return story_board
    except Exception as e:
        logger.error(f"Failed to generate story board: {e}")
        raise


async def slide_creator(slide_template: dict, html_template: dict, page_name:str) -> List[Dict]:
    """Create slides with images and handle errors gracefully"""
    try:
        session_id = str(uuid.uuid4())[:8]
        name = slide_template["name"]
        text = slide_template["text"]

        # Generate images from different sources
        image_tasks = [
            fetch_multiple_images(
                headline=slide_template["image_description"],
                reference_image=None,
                session_id=session_id,
            ),
            generate_single_image(
                headline=slide_template["image_description"],
                session_id=session_id,
                model="gpt-image-1",
            ),
            # generate_single_image(
            #     headline=slide_template['image_description'],
            #     session_id=session_id,
            #     model="imagen-4.0-ultra-generate-preview-06-06"
            # ),
        ]

        results = await asyncio.gather(*image_tasks, return_exceptions=True)

        # Process results and handle individual failures
        all_images = []

        # Collect all successful images
        # Real images from fetch_multiple_images
        if not isinstance(results[0], Exception) and results[0]:
            for img in results[0]:
                img["type"] = "real"
                all_images.append(img)

        # Generated images from AI models
        for result in results[1:]:
            if isinstance(result, Exception) or not result:
                continue
            
            # Handle both single images and lists
            images_to_add = result if isinstance(result, list) else [result]
            for img in images_to_add:
                img["type"] = "generated"
                all_images.append(img)

        # If no images were generated, return empty list
        if not all_images:
            logger.warning(
                f"No images generated for slide: {slide_template.get('name', 'unknown')}"
            )
            return []

        # Process all images in parallel
        async def process_image(img_data):
            """Add text overlay to image"""
            try:
                session_id = str(uuid.uuid4())[:8]
                file_name = f"background_image_{session_id}.png"
                file_path = f"./data/{page_name}/temp/{file_name}"
                
                with open(file_path, "wb") as f:
                    f.write(img_data["image_bytes"])
                loop = asyncio.get_event_loop()
                with_text_bytes = await loop.run_in_executor(
                    None,
                    text_editor,
                    html_template[name],
                    page_name,
                    {"crop_type": "cover"},
                    {},
                    text,
                    {"background_image": file_path},
                    session_id,
                    False,
                )
                
                return {
                    "images": {
                        "without_text": img_data["image_bytes"],
                        "with_text": with_text_bytes
                    },
                    "type": img_data["type"],
                    "model": img_data.get("model", "unknown")
                }
            except Exception as e:
                logger.warning(f"Failed to process image: {e}")
                return None

        # Process all images concurrently and filter out failures
        tasks = [process_image(img) for img in all_images]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        processed_images = [r for r in results if r and not isinstance(r, Exception)]

        return processed_images

    except Exception as e:
        logger.error(f"Error in slide_creator: {e}")
        return []


async def text_only_slide_creator(slide_template: dict, html_template: dict, page_name:str) -> List[Dict]:
    session_id = str(uuid.uuid4())[:8]
    name = slide_template["name"]
    text = slide_template["text"]

    loop = asyncio.get_event_loop()
    with_text_bytes = await loop.run_in_executor(
                    None,
                    text_editor,
                    html_template[name],
                    page_name,
                    {},
                    {},
                    text,
                    {},
                    session_id,
                    False,
                )
    
    return [{
                    "images": {
                        "without_text": None,
                        "with_text": with_text_bytes
                    },
                    "type": "text",
                    "model": "unknown"
            }]


async def save_to_mongo(session_id: str, headline: str, template_type: str, 
                      story_board: dict, slide_images: list, page_name: str = "scoopwhoop", error: str = None) -> str:
    """Save workflow results to MongoDB"""
    try:
        mongo_client = get_mongo_client()
        document_id = mongo_client.store_content_workflow(
            session_id=session_id,
            headline=headline,
            template_type=template_type,
            story_board=story_board,
            slide_images=slide_images,
            page_name=page_name,
            error=error,
        )
        mongo_client.close()
        logger.info(f"Saved to MongoDB: {document_id}")
        return document_id
    except Exception as e:
        logger.error(f"MongoDB save failed: {e}")
        raise


async def workflow(headline: str, template: dict,image_bytes: bytes = None, save: bool = True) -> str:
    """Main workflow function that creates content and optionally saves to MongoDB"""
    session_id = str(uuid.uuid4())[:8]

    try:
        # Generate story board
        story_board = await story_board_creator(
            headline=headline, text_template=template["text_template"],image_bytes=image_bytes
        )
        # Generate all slides in parallel using threads
        slides = story_board.get("storyboard", [])
        if not slides:
            slide_results = []
        else:
            def create_slide(slide):
                """Run slide creator in thread"""
                if slide.get("image_description", None) is None:
                    return asyncio.run(text_only_slide_creator(slide, template["slides"], template["page_name"]))
                else:
                    return asyncio.run(slide_creator(slide, template["slides"], template["page_name"]))

            # Run each slide in its own thread
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=3) as executor:
                tasks = [loop.run_in_executor(executor, create_slide, slide) for slide in slides]
                try:
                    results = await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=300) # 5 min timeout
                except asyncio.TimeoutError:
                    logger.error("Slide generation timed out after 5 minutes")
                    results = [TimeoutError(f"Slide {i} timed out") for i in range(len(slides))]
                
                # Handle failures
                slide_results = []
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        logger.error(f"Slide {i} failed: {result}")
                        slide_results.append([])
                    else:
                        slide_results.append(result)

        # Save to MongoDB if requested
        if save:
            document_id = await save_to_mongo(
                session_id=session_id,
                headline=headline,
                template_type=template["template_type"],
                story_board=story_board,
                slide_images=slide_results,
                page_name=template["page_name"],
                error=None,
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
                    template_type=template.get("template_type", "unknown"),
                    story_board={"storyboard": []},
                    slide_images=[],
                    page_name=template.get("page_name", "scoopwhoop"),
                    error=str(e),
                )
            except Exception as mongo_error:
                logger.error(f"Failed to save error state to MongoDB: {mongo_error}")

        return session_id


if __name__ == "__main__":
    import asyncio
    import base64
    # from src.templates.timeline import timeline_template
    # from src.templates.twitter.tweet_image import tweet_image_template
    from src.templates.the_sarcastic_indian.writeup import writeup_template

    headline = "UttarKashi Cloud Burst India"

    try:
        session_id = asyncio.run(workflow(headline=headline, template=writeup_template,save=True))
        # session_id = "5a935915"
        print(f"Workflow completed successfully!")
        print(f"Document ID: {session_id}")
        mongo_client = get_mongo_client()
        result = mongo_client.get_workflow_result(session_id)
        for slide in result["slides"]:
            for img in slide["images"]:
                b64_img = base64.b64decode(img["images"]["with_text"]["image_base64"])
                with open(
                    f"./data_/slide_1/test_{slide['slide_index']}.png", "wb"
                ) as f:
                    f.write(b64_img)
        mongo_client.close()
    except Exception as e:
        print(f"Workflow failed: {e}")
