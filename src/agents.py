import json
import string
from typing import List, Tuple

from src.prompts import IMAGE_DESCRIPTION_PROMPT, COPY_EXTRACTOR_PROMPT, TEMPLATE_PROMPT, HTML_TEMPLATE_PROMPT
from src.utils import extract_x, capture_html_screenshot
from src.clients import openai_response, openai_image_response

async def copy_extractor(image:List[str] = []) -> str:
    prompt = COPY_EXTRACTOR_PROMPT
    response = await openai_response(prompt=prompt, images=image, model = "gpt-4.1")
    return json.loads(extract_x(response,"json"))

async def html_template_generator(image:List[str] = [], analysis:dict = {}) -> str:
    prompt = TEMPLATE_PROMPT.format(analysis)
    response = await openai_response(prompt=prompt, images=image, model = "gpt-4.1")
    input_json = json.loads(extract_x(response,"json"))
    html_template = HTML_TEMPLATE_PROMPT.format(**input_json)
    return html_template

async def image_generator(query:str = "") -> str:
    prompt = IMAGE_DESCRIPTION_PROMPT.format(query)
    response = await openai_image_response(prompt=prompt)
    return response

async def test_workflow() -> None:
    analysis = await copy_extractor(image=["./data/scoopwhoop/analyze.png"])
    image = await image_generator(query=analysis["headline"])

    with open("./data/scoopwhoop/generated_image.png", "wb") as f:
        f.write(image)
    
    html_template = await html_template_generator(image=["./data/scoopwhoop/generated_image.png"], analysis=analysis)
    with open("./data/scoopwhoop/html_template.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    capture_html_screenshot(file_path="./data/scoopwhoop/html_template.html",element_selector=".container",output="./data/scoopwhoop/generated_image_with_text.png")

if __name__ == "__main__":
    import asyncio
    print(asyncio.run(test_workflow()))