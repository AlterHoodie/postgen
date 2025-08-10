import logging
from typing import List, Dict
import json

from src.agents import (
    image_desc_generator,
    image_generator,
    image_query_creator,
    image_search_agent,
)

logger = logging.getLogger(__name__)


async def generate_single_image(
    headline: str, session_id: str, model: str
) -> Dict[str, str]:
    """Process a single image: generate, save, create HTML, and capture screenshot

    Returns:
        Tuple of (image_paths_dict, temp_files_list)
        image_paths_dict contains both 'without_text' and 'with_text' image paths
    """

    try:
        # Generate image from description
        with open("./data_/test.png", "rb") as f:
            image_bytes = f.read()
            return {
                "type": "real",
                "model": "test",
                "description": None,
                "image_bytes": image_bytes,
            }
        image_descriptions = await image_desc_generator(query=headline)
        image_bytes = await image_generator(query=image_descriptions[0], model=model)

        if not image_bytes:
            raise Exception("No image bytes generated - likely due to moderation")

        return {
            "type": "generated",
            "model": model,
            "description": image_descriptions[0],
            "image_bytes": image_bytes,
        }

    except Exception as e:
        logger.error(f"Error processing generated image {model} {session_id}: {e}")
        return {
            "type": "generated",
            "model": model,
            "description": None,
            "image_bytes": None,
            "error": str(e),
        }


async def fetch_multiple_images(
    headline: str, session_id: str, reference_image: bytes = None
) -> List[Dict[str, str]]:
    """Process a single image: generate, save, create HTML, and capture screenshot

    Returns:
        Tuple of (image_paths_dict, temp_files_list)
        image_paths_dict contains both 'without_text' and 'with_text' image paths
    """
    try:
        with open("./data_/test.png", "rb") as f:
            image_bytes = f.read()
            return [
                {
                    "type": "real",
                    "model": "test",
                    "description": None,
                    "image_bytes": image_bytes,
                }
            ]
        image_query = await image_query_creator(
            headline=headline, image=reference_image
        )

        # Generate image from description
        image_list = await image_search_agent(
            query=image_query["queries"][0], reference_image=reference_image
        )

        return [
            {
                "type": "real",
                "model": "google_search",
                "description": {
                    "query": image_query["queries"][0],
                    "image_url": image["image_url"],
                    "image_description": image["image_description"],
                    "image_source": image["image_source"],
                    "image_cite": image["image_cite"],
                },
                "image_bytes": image["image_data"].getvalue(),
            }
            for image in image_list
        ]

    except Exception as e:
        logger.error(f"Error processing real image {session_id}: {e}")
        return []


if __name__ == "__main__":
    import asyncio
    from uuid import uuid4

    session_id = str(uuid4())[:8]
    result = asyncio.run(
        fetch_multiple_images(
            headline="Rahul Gandhi Alleges Voter Fraud in Bengaluru",
            reference_image=None,
            session_id=session_id,
        )
    )
    with open("./data_/test_out.png", "wb") as f:
        f.write(result[0]["image_bytes"])
