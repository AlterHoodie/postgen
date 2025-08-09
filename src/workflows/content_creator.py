import logging
from typing import List, Dict
import json
import asyncio
import uuid

from src.agents import story_board_generator
from src.workflows.image_gen import fetch_multiple_images, generate_single_image
from src.workflows.editors import image_editor

logger = logging.getLogger(__name__)

async def story_board_creator(headline:str, template:str) -> List[Dict[str, str]]:  
    try:
        story_board = await story_board_generator(headline=headline, template=template)
        return story_board
    except Exception as e:
        logger.error(f"Error generating story board: {e}")
        raise Exception(f"Error generating story board: {e}")

async def slide_creator(slide_template:dict, html_template:dict) -> Dict[str, str]:
    try:
        session_id = str(uuid.uuid4())[:8]
        image_tasks = [
            fetch_multiple_images(headline=slide_template['image_description'], reference_image=None, session_id=session_id),
            # generate_single_image(headline=slide_template['image_description'], model="gpt-image-1"),
            # generate_single_image(headline=slide_template['image_description'], model="imagen-4.0-ultra-generate-preview-06-06"),
        ]

        # # results = await asyncio.gather(*image_tasks)
        # with open("./data_/test.png", "rb") as f:
        #     results = [[{"image_bytes":f.read()}]]
        results = await asyncio.gather(*image_tasks)
        image_results = results[0]
        images = []
        for result in image_results:
            image_bytes = image_editor(image_bytes=result['image_bytes'], text_template = slide_template['text_template'], html_template = html_template[slide_template['name']])
            images.append(image_bytes)

        return images
    except Exception as e:
        logger.error(f"Error generating slide: {e}")
        raise Exception(f"Error generating slide: {e}")

async def workflow(headline:str, template:str) -> List[Dict[str, str]]:
    try:
        story_board = await story_board_creator(headline=headline, template=template['text_template'])

        # Create tasks to run in thread pool
        loop = asyncio.get_event_loop()
        tasks = []
        results = []
        for slide in story_board['storyboard']:
            result = await slide_creator(
                slide_template=slide,
                html_template=template['html_template']
            )
            results.append(result)

        return story_board, results

    except Exception as e:
        logger.error(f"Error fetching images: {e}")
        raise Exception(f"Error fetching images: {e}")


if __name__ == "__main__":
    import asyncio
    from src.templates.timeline import TEXT_TEMPLATE,HEADLINE_SLIDE_HTML_TEMPLATE, TIMELINE_START_SLIDE_TEMPLATE, TIMELINE_MIDDLE_SLIDE_TEMPLATE, TIMELINE_END_SLIDE_TEMPLATE
    template = {
        "text_template":TEXT_TEMPLATE,
        "html_template":{
            "headline_slide":HEADLINE_SLIDE_HTML_TEMPLATE,
            "timeline_start_slide":TIMELINE_START_SLIDE_TEMPLATE,
            "timeline_middle_slide":TIMELINE_MIDDLE_SLIDE_TEMPLATE,
            "timeline_end_slide":TIMELINE_END_SLIDE_TEMPLATE
        }
    }

    headline = "UttarKashi Cloud Burst India"

    story_board, results = asyncio.run(workflow(headline=headline, template=template))

    print(json.dumps(story_board, indent=4))

    for idx, result in enumerate(results):
        with open(f"./data_/slide/test_{idx}.png", "wb") as f:
            f.write(result[0])