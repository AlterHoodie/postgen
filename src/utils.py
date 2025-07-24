import re
from pathlib import Path
import time
import logging
import os
from typing import List
import io
from PIL import Image
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

def pil_image_to_bytes(image, format='PNG'):
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    return buffer.getvalue()

def compress_image(image_data: bytes, max_size: tuple = (1200, 1800), quality: int = 80) -> bytes:
    """
    Compress an image while maintaining aspect ratio and quality.
    
    Args:
        image_data: Raw image bytes
        max_size: Maximum dimensions (width, height) for the image
        quality: JPEG quality (1-100, higher is better quality)
        
    Returns:
        Compressed image bytes
        
    Example:
        ```python
        with open("image.jpg", "rb") as f:
            image_bytes = f.read()
        compressed_bytes = compress_image(image_bytes)
        ```
    """
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Calculate new dimensions while maintaining aspect ratio
        ratio = min(max_size[0] / img.width, max_size[1] / img.height)
        if ratio < 1:  # Only resize if image is larger than max_size
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
        # Save compressed image to bytes
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
        
    except Exception as e:
        print(f"Error compressing image: {e}")
        return image_data  # Return original if compression fails



if __name__ == "__main__":
    capture_html_screenshot(file_path="./data/scoopwhoop/html_template.html",element_selector=".container")
