import json
import string
from typing import List, Tuple

from src.prompts import HTML_TEMPLATE_PROMPT, IMAGE_DESCRIPTION_PROMPT, INPUT_TEMPLATE_PROMPT, COPY_EXTRACTOR_PROMPT, IMAGE_DESCRIPTION_WITH_TEXT_PROMPT
from src.utils import extract_x
from src.clients import openai_response, openai_image_response, anthropic_response



def extract_input_json(template):
    formatter = string.Formatter()
    keys = {field_name: "<value>" for _, field_name, _, _ in formatter.parse(template) if field_name}
    return keys

async def html_template_generator(image:List[str] = [], analysis:dict = {}) -> Tuple[str, str]:
    prompt = HTML_TEMPLATE_PROMPT.format(analysis)

    response = await anthropic_response(images = image, prompt=prompt, model = "claude-sonnet-4-20250514")
    # response = await openai_response(prompt=prompt, model = "gpt-4.1",images=image)

    return extract_x(response,"html"), extract_input_json(extract_x(response,"html"))

async def image_generator(query:str = "") -> str:
    prompt = IMAGE_DESCRIPTION_PROMPT.format(query)
    response = await openai_response( prompt=prompt, model = "gpt-4.1",images=[])

    response = await openai_image_response(prompt=response)
    return response

async def image_generator_with_text(query:str = "",image:str = "") -> str:
    prompt = IMAGE_DESCRIPTION_WITH_TEXT_PROMPT.format(query)
    response = await openai_response(prompt=prompt, model = "gpt-4.1")
    response = await openai_image_response(prompt=response,images=[image])
    return response

async def copy_extractor(image:List[str] = []) -> str:
    prompt = COPY_EXTRACTOR_PROMPT
    response = await openai_response(prompt=prompt, images=image, model = "gpt-4.1")
    return json.loads(extract_x(response,"json"))

async def html_input_generator(image: List[str] = [], headline:str = "", json_template:dict = {}) -> str:
    json_template = json_template.copy()
    del json_template["background_image_url"]
    del json_template["logo_url"]
    prompt = INPUT_TEMPLATE_PROMPT.format(headline, json_template)
    response = await openai_response(prompt=prompt, images=image, model = "gpt-4.1")
    return json.loads(extract_x(response,"json"))

async def test_workflow() -> None:
    analysis = await copy_extractor(image=["./data/scoopwhoop/analyze.png"])
    images = ["./data/scoopwhoop/sample.png"]
    html_template, json_template = await html_template_generator(image=images, analysis=analysis)

    with open("./data/scoopwhoop/html_template.html", "w") as f:
        f.write(html_template)
    with open("./data/scoopwhoop/json_template.json", "w") as f:
        json.dump(json_template, f, indent=4)

    image = await image_generator(query=analysis["headline"])
    with open("./data/scoopwhoop/generated_image.png", "wb") as f:
        f.write(image)
    
    background_image_url = "./data/scoopwhoop/generated_image.png"
    logo_url = "./data/scoopwhoop/logo.png"

    json_input_template = await html_input_generator(image=[background_image_url], headline=analysis["headline"], json_template=json_template)

    with open("./data/scoopwhoop/bleh_1.html", "w", encoding="utf-8") as f:
        f.write(html_template.format(background_image_url=background_image_url, logo_url=logo_url, **json_input_template))

async def test_workflow_with_text() -> None:
    analysis = await copy_extractor(image=["./data/scoopwhoop/analyze.png"])
    image_with_text, image = await asyncio.gather(
        image_generator_with_text(query=analysis["headline"], image="./data/scoopwhoop/text_sample.png"),
        image_generator(query=analysis["headline"])
    )

    with open("./data/results_2/generated_image_with_text.png", "wb") as f:
        f.write(image_with_text)
    with open("./data/results_2/generated_image.png", "wb") as f:
        f.write(image)

if __name__ == "__main__":
    import asyncio
    # print(asyncio.run(test_workflow()))
    print(asyncio.run(test_workflow_with_text()))