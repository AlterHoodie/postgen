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

def extract_text_from_html(html_content):
    """Extract headline and sub_text from HTML content"""
    try:
        # Extract headline (h1 content)
        headline_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.DOTALL)
        headline = headline_match.group(1).strip() if headline_match else ""
        
        # Extract sub_text (p content) 
        subtext_match = re.search(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
        sub_text = subtext_match.group(1).strip() if subtext_match else ""
        
        return headline, sub_text
    except Exception as e:
        logger.error(f"Error extracting text from HTML: {e}")
        return "", ""

def regenerate_image_from_html(html_content, session_id, image_index, original_image_data=None):
    """Regenerate image from modified HTML content"""
    try:
        # Create temporary HTML file
        temp_dir = Path("./data/scoopwhoop/temp")
        temp_dir.mkdir(exist_ok=True)
        
        temp_html_path = f"./data/scoopwhoop/temp/edited_html_{session_id}_{image_index}_{uuid.uuid4().hex[:8]}.html"
        temp_bg_image_name = f"bg_image_{session_id}_{image_index}_{uuid.uuid4().hex[:8]}.png"
        temp_bg_image_path = f"./data/scoopwhoop/temp/{temp_bg_image_name}"
        temp_image_path = f"./data/scoopwhoop/temp/edited_image_{session_id}_{image_index}_{uuid.uuid4().hex[:8]}.png"
        # Extract background image src from HTML
        # Use BeautifulSoup for reliable HTML parsing
        soup = BeautifulSoup(html_content, 'html.parser')
        background_image_tag = soup.find('img', class_='background-image')
        background_image_src = background_image_tag.get('src') if background_image_tag else None
        
        if background_image_src and original_image_data:
            
            try:
                # Get the image data from the original data (without text version)
                if "images" in original_image_data and "without_text" in original_image_data["images"]:
                    bg_image_b64 = original_image_data["images"]["without_text"]["image_base64"]
                    bg_image_bytes = base64.b64decode(bg_image_b64)
                    
                    # Write background image to temp location
                    with open(temp_bg_image_path, "wb") as f:
                        f.write(bg_image_bytes)
                    
                    # Update HTML to point to the correct background image path
                    
                    # Use BeautifulSoup for reliable HTML modification
                    background_image_tag['src'] = temp_bg_image_name
                    html_content = str(soup)
                    
                    logger.info(f"Downloaded background image to: {temp_bg_image_path}")
                    
            except Exception as e:
                logger.warning(f"Failed to extract background image: {e}")
        
        # Write HTML to file
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Capture screenshot
        capture_html_screenshot(
            file_path=temp_html_path,
            element_selector=".container",
            output=temp_image_path
        )
        
        # Read the generated image
        with open(temp_image_path, "rb") as f:
            image_bytes = f.read()
        
        # Clean up temporary files
        Path(temp_html_path).unlink(missing_ok=True)
        Path(temp_image_path).unlink(missing_ok=True)
        Path(temp_bg_image_path).unlink(missing_ok=True)
        return image_bytes
    
    except Exception as e:
        logger.error(f"Error regenerating image: {e}")
        return None

def update_html_content(original_html, new_headline, new_sub_text):
    """Update HTML content with new headline and sub_text"""
    try:
        # Replace headline
        updated_html = re.sub(
            r'(<h1[^>]*>)(.*?)(</h1>)', 
            fr'\1{new_headline}\3', 
            original_html, 
            flags=re.DOTALL
        )
        
        # Replace sub_text
        updated_html = re.sub(
            r'(<p[^>]*>)(.*?)(</p>)', 
            fr'\1{new_sub_text}\3', 
            updated_html, 
            flags=re.DOTALL
        )
        
        return updated_html
    except Exception as e:
        logger.error(f"Error updating HTML content: {e}")
        return original_html


if __name__ == "__main__":
    capture_html_screenshot(file_path="./data/scoopwhoop/html_template.html",element_selector=".container")
