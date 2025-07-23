import re
from pathlib import Path
import time
import logging
import os
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)

def extract_x(response: str, code_type: str) -> str:
    pattern = rf"```{code_type}\s*(.*?)```"
    match = re.search(pattern, response, re.DOTALL)
    return match.group(1).strip() if match else None

def cleanup_files(file_paths: List[str]) -> None:
    """Delete all temporary files generated during the workflow"""
    # print(file_paths)
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                if "logo.png" in file_path:
                    continue
                os.remove(file_path)
                logger.info(f"Deleted temporary file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to delete file {file_path}: {e}")



def capture_html_screenshot(
    file_path: str,
    element_selector: str,
    output: str = "./data/scoopwhoop/element_screenshot.png",
    zoom: float = 1.0,
    delay: float = 0.5,
    headless: bool = True
):
    file_url = Path(file_path).resolve().as_uri()

    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--window-size=1920,2000")

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(file_url)

        # Apply zoom if needed
        if zoom != 1.0:
            driver.execute_script(f"document.body.style.zoom='{zoom}';")
        
        time.sleep(delay)

        # Find the element (e.g., an <img> tag)
        element = driver.find_element("css selector", element_selector)

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.2)

        # Capture screenshot of the element
        element.screenshot(output)
        logger.info(f"Image element captured and saved to {output}")
    except Exception as e:
        logger.error(f"Error capturing image element: {e}")
        raise e
    finally:
        driver.quit()


if __name__ == "__main__":
    capture_html_screenshot(file_path="./data/scoopwhoop/html_template.html",element_selector=".container")
