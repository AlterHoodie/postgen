import json
import logging
from typing import List

from src.prompts import IMAGE_DESCRIPTION_PROMPT, COPY_EXTRACTOR_PROMPT, TEMPLATE_PROMPT, HTML_TEMPLATE_PROMPT
from src.utils import extract_x
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

if __name__ == "__main__":
    import asyncio
    print(asyncio.run(copy_extractor(image=["./data/image.png"])))