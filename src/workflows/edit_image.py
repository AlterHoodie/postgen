import uuid
from pathlib import Path

from src.prompts import HTML_TEMPLATE_PROMPT_REAL
from src.utils import convert_simple_text_to_html, capture_html_screenshot, cleanup_files


def image_workflow(image_bytes, subtext, headline="", source="",is_trigger=False):
    try:
        temp_dir = Path("./data/scoopwhoop/temp")
        temp_dir.mkdir(exist_ok=True)

        temp_files = []
        html_tags = []

        headline_html, subtext_html = convert_simple_text_to_html(headline, subtext)

        if is_trigger:
            html_tags.append("<div class='trigger-warning'>Trigger Warning</div>")

        if headline:
            html_tags.append(headline_html)
            html_tags.append(subtext_html)
        else:
            html_tags.append(subtext_html)

        if source:
            html_tags.append(f"<p class='source'>Source: {source}</p>")

        session_id = str(uuid.uuid4())[:8]
        input_image_name = f"input_image_{session_id}.png"
        input_image_path = f"./data/scoopwhoop/temp/{input_image_name}"
        with open(input_image_path, "wb") as f:
            f.write(image_bytes)
        temp_files.append(input_image_path)

        html_path = f"./data/scoopwhoop/temp/temp_overlay_{session_id}.html"
        html_content = HTML_TEMPLATE_PROMPT_REAL.format(
            file_path=input_image_name,
            html_snippet_code="\n".join(html_tags)
        )
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        temp_files.append(html_path)

        overlay_image_path = f"./data/scoopwhoop/temp/overlay_{session_id}.png"
        capture_html_screenshot(
            file_path=html_path,
            element_selector=".container",
            output=overlay_image_path,
        )
        temp_files.append(overlay_image_path)

        with open(overlay_image_path, "rb") as f:
                return f.read()
    except Exception as e:
        print(f"Error in workflow: {e}")
        return None
    finally:
        cleanup_files(temp_files)

if __name__ == "__main__":
    with open("./data_/test.png", "rb") as f:
        image_bytes = f.read()
    result = image_workflow(
        image_bytes=image_bytes,
        # headline="**India Post** goes digital. A **smarter era** begins.",
        subtext="No more snail mail—India Post goes digital. A smarter era begins.",
        # is_trigger=True,
        source="Financial Express"
    )
    with open("./data_/test_out.png", "wb") as f:
        f.write(result)