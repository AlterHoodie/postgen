import re
from pathlib import Path
import time
import logging
import os
from typing import List
import io
import uuid
import shutil
import base64

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


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
    delay: float = 0.2,
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

def crop_image(
    image_bytes: bytes,
    output_width: int = 1080,
    output_height: int = 1350,
    bias: float = 0.35
) -> bytes:
    """
    Crops an image to the specified size with subject-biased centering.

    Args:
        image_path: Path to the input image.
        output_path: Path to save the cropped image.
        output_width: Target width (default 1080).
        output_height: Target height (default 1350).
        bias: Bias from center to keep subject in view (0 = left-aligned, 0.5 = center, 1 = right-aligned).

    Returns:
        Path to the cropped image.
    """
    img = Image.open(io.BytesIO(image_bytes))
    scale_factor = output_height / img.height
    resized_width = int(img.width * scale_factor)
    resized_img = img.resize((resized_width, output_height), Image.Resampling.LANCZOS)

    left = int((resized_width - output_width) * bias)
    top = 0
    right = left + output_width
    bottom = output_height

    cropped = resized_img.crop((left, top, right, bottom))
    buffer = io.BytesIO()
    cropped.save(buffer,format="PNG")

    return buffer.getvalue()

def convert_simple_text_to_html(headline_text, subtext_text):
    """Convert simple text with **text** syntax to styled HTML"""
    try:
        # Process headline
        headline_lines = headline_text.strip().split('\n')
        headline_html_parts = []
        
        for line in headline_lines:
            line = line.strip()
            if line:
                # Replace **text** syntax with yellow spans
                processed_line = re.sub(
                    r'\*\*([^*]+?)\*\*', 
                    r'<span class="yellow">\1</span>', 
                    line
                )
                headline_html_parts.append(processed_line)
        
        # Join with <br /> tags
        headline_html = f"<h1>\n    {('<br />').join(headline_html_parts)}\n</h1>"
        
        # Process sub-text
        subtext_lines = subtext_text.strip().split('\n')
        subtext_html_parts = []
        
        for line in subtext_lines:
            line = line.strip()
            if line:
                # Replace **text** syntax with yellow spans
                processed_line = re.sub(
                    r'\*\*([^*]+?)\*\*', 
                    r'<span class="yellow">\1</span>', 
                    line
                )
                subtext_html_parts.append(processed_line)
        
        # Join with <br /> tags
        subtext_html = f"<p class='subtext'>{('<br />').join(subtext_html_parts)}</p>"
        
        return headline_html, subtext_html
        
    except Exception as e:
        logger.error(f"Error converting simple text to HTML: {e}")
        return f"<h1>{headline_text}</h1>", f"<p>{subtext_text}</p>"

def extract_text_from_html(html_content):
    """Extract clean text from HTML content, converting spans to **text** syntax"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Convert yellow spans to **text** syntax
        for span in soup.find_all('span', class_='yellow'):
            span.replace_with(f"**{span.get_text()}**")
        
        # Get text content, replace <br/> with newlines
        text = soup.get_text(separator=' ').strip()
        text = re.sub(r'<br\s*/?>', '\n', text)
        return text
    except Exception as e:
        logger.error(f"Error extracting text from HTML: {e}")
        return "", ""


if __name__ == "__main__":
    print(convert_simple_text_to_html("""POV: When Your **Wallet** has more **Personality** than **Money**""","UPI Id in the description, please **gib money**")[1])
    # # with open("./data_/test_cropped.png","wb") as f:
    # #     f.write(crop_image(image_bytes=open("./data_/test.png","rb").read(),bias=0.5))
    # capture_html_screenshot(file_path="./data_/overlay_test.html",element_selector=".container",output="./data_/test_out.png",delay=0.1,headless=True)
