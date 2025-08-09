import logging
import uuid
from pathlib import Path
from typing import Tuple

from PIL import Image, ImageDraw
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

from src.utils import capture_html_screenshot, cleanup_files

logger = logging.getLogger(__name__)

def image_editor(image_bytes:bytes, text_template:dict, html_template:str) -> bytes:
    try:
        temp_dir = Path("./data/scoopwhoop/temp")
        temp_dir.mkdir(exist_ok=True)
        temp_files = []
        session_id = str(uuid.uuid4())[:8]

        input_image_name = f"input_image_{session_id}.png"
        input_image_path = f"./data/scoopwhoop/temp/{input_image_name}"
        with open(input_image_path, "wb") as f:
            f.write(image_bytes)
        
        temp_files.append(input_image_path)

        html_path = f"./data/scoopwhoop/temp/temp_overlay_{session_id}.html"
        html_content = html_template.format(
            file_path=input_image_name,
            **text_template
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
        logger.error(f"Error in workflow: {e}")
        return None
    finally:
        cleanup_files(temp_files)

def create_gradient_overlay(width:int, height:int, gradient_height_ratio:float=0.35) -> Image:
    """
    Create a gradient overlay image that's transparent at top and black at bottom
    """
    gradient_height = int(height * gradient_height_ratio)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    
    for y in range(gradient_height):
        alpha = int(y*1.7)
        draw = ImageDraw.Draw(img)
        y_pos = height - gradient_height + y
        draw.line([(0, y_pos), (width, y_pos)], fill=(0, 0, 0, alpha))
    
    return img

def process_overlay_for_transparency(image_path:str, session_id:str, target_width:int=576, target_height:int=720) -> str:
    """
    Process overlay image to make black areas transparent
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        pixels = img.getdata()
        new_pixels = []

        for pixel in pixels:
            r, g, b, a = pixel
            if r == 0 and g == 0 and b == 0:
                new_pixels.append((255, 255, 255, 0))  # Make black transparent
            else:
                new_pixels.append(pixel)

        img.putdata(new_pixels)
        resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        output_path = f"./data/scoopwhoop/temp/processed_overlay_{session_id}.png"
        resized_img.save(output_path, format="PNG")
        return output_path
    
    except Exception as e:
        logger.error(f"Error processing overlay image Error: {e}")
        return None


def create_overlay_image(text_template:dict, html_template:str, session_id:str) -> Tuple[str, str]:
    """
    Create the overlay image with text using HTML template
    """
    # Save HTML template
    html_content = html_template.format(**text_template)
    html_path = f"./data/scoopwhoop/temp/temp_overlay_{session_id}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Create overlay image from HTML
    overlay_image_path = f"./data/scoopwhoop/temp/overlay_{session_id}.png"
    capture_html_screenshot(
        file_path=html_path,
        element_selector=".container",
        output=overlay_image_path,
    )
    
    return overlay_image_path, html_path


def create_final_video(video_path:str, overlay_image_path:str, session_id:str, target_width:int=576, target_height:int=720, add_gradient:bool=True) -> Tuple[bytes, str]:
    """
    Create final video with fixed size scaling to 576x720
    """
    try:
        video_clip = VideoFileClip(video_path)
        (original_width, original_height) = video_clip.size
        
        # STEP 1: Crop to 4:5 ratio first
        target_ratio = 4 / 5  # 576/720 = 0.8
        original_ratio = original_width / original_height
        
        if original_ratio > target_ratio:
            # Video is wider - crop width to match 4:5 ratio
            crop_height = original_height
            crop_width = int(crop_height * target_ratio)
        else:
            # Video is taller - crop height to match 4:5 ratio
            crop_width = original_width
            crop_height = int(crop_width / target_ratio)
        
        # Crop to 4:5 ratio first
        cropped_clip = video_clip.cropped(
            width=crop_width,
            height=crop_height,
            x_center=original_width / 2,
            y_center=original_height / 2
        )
        
        # STEP 2: Scale to exact target dimensions (576x720)
        final_clip = cropped_clip.resized((target_width, target_height))
        
        # Create list of clips to composite
        clips_to_composite = [final_clip]
        
        # Add gradient overlay if requested
        if add_gradient:
            gradient_img = create_gradient_overlay(target_width, target_height)
            gradient_path = f"./data/scoopwhoop/temp/gradient_{session_id}.png"
            gradient_img.save(gradient_path, "PNG")
            
            gradient_clip = ImageClip(gradient_path).with_duration(final_clip.duration)
            clips_to_composite.append(gradient_clip)
        else:
            gradient_path = None
        
        # Process overlay image to match target dimensions
        overlay_img = Image.open(overlay_image_path)
        overlay_resized = overlay_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        overlay_resized_path = f"./data/scoopwhoop/temp/overlay_resized_{session_id}.png"
        overlay_resized.save(overlay_resized_path, "PNG")
        
        overlay_clip = ImageClip(overlay_resized_path)
        overlay_clip = overlay_clip.with_duration(final_clip.duration)
        clips_to_composite.append(overlay_clip.with_position("center"))
        
        # Composite all clips together
        final_composite = CompositeVideoClip(clips_to_composite)
        output_path = f"./data/scoopwhoop/temp/final_video_{session_id}.mp4"
        
        # Write the final file
        final_composite.write_videofile(
            output_path, 
            codec='libx264', 
            audio_codec='aac', 
            threads=4, 
            fps=15,
            preset='ultrafast', 
            bitrate='1500k', 
            audio_bitrate='128k',
            logger=None,
        )
        
        # Close clips to free memory
        video_clip.close()
        final_composite.close()
        
        return output_path, [overlay_resized_path, gradient_path]
        
    except Exception as e:
        print(f"Error during video processing: {e}")
        return None


def video_editor(video_bytes:bytes, text_template:dict, html_template:str) -> bytes:
    """
    Complete workflow to create edited video with text overlay
    
    Args:
        video_bytes: Raw video file bytes
        headline: Main headline text
        subtext: Subtitle text
        
    Returns:
        str: Path to the final video file, or None if failed
    """
    session_id = str(uuid.uuid4())[:8]
    temp_files = []
    
    try:
        # Create temp directory
        temp_dir = Path("./data/scoopwhoop")
        temp_dir.mkdir(exist_ok=True)
        
        # Step 1: Save input video
        input_video_path = f"./data/scoopwhoop/temp/input_video_{session_id}.mp4"
        with open(input_video_path, "wb") as f:
            f.write(video_bytes)
        temp_files.append(input_video_path)
        
        # Step 2: Create the overlay image with text
        overlay_image_path, html_path = create_overlay_image(
            text_template=text_template,
            html_template=html_template,
            session_id=session_id
        )
        temp_files.extend([overlay_image_path, html_path])
        
        processed_overlay_path = process_overlay_for_transparency(
            image_path=overlay_image_path,
            session_id=session_id,
            target_width=576,
            target_height=720
        )
        
        # Step 4: Create the final video (576x720)
        final_video_path, video_temp_files = create_final_video(
            video_path=input_video_path,
            overlay_image_path=processed_overlay_path,
            session_id=session_id,
            add_gradient=True,
            target_width=576,
            target_height=720
        )
        temp_files.extend(video_temp_files)
        
        if not final_video_path:
            logger.error("Failed to create final video")
            raise Exception("Failed to create final video")
        
        logger.info(f"Workflow completed successfully: {final_video_path}")
        with open(final_video_path, "rb") as f:
            temp_files.append(final_video_path)
            return f.read()
        
    except Exception as e:
        logger.error(f"Error in workflow: {e}")
        raise Exception(f"Error in workflow: {e}")
        
    finally:
        # Step 5: Clean up temp files
        cleanup_files(temp_files)
        logger.info(f"Cleaned up {len(temp_files)} temporary files")


# Test function for development
if __name__ == "__main__":
    from src.templates.basic import HTML_TEMPLATE_PROMPT_REAL
    ## Test Image Workflow
    with open("./data_/test.png", "rb") as f:
        image_bytes = f.read()
    result = image_editor(
        image_bytes=image_bytes,
        text_template={
            "headline": "<h1><span class='yellow'>India Post</span> goes digital. A <span class='yellow'>smarter era</span> begins.</h1>",
            "subtext": "<p class='subtext'>No more snail mail—India Post goes digital. A smarter era begins.</p>",
            "is_trigger": ""
        },
        html_template=HTML_TEMPLATE_PROMPT_REAL
    )
    with open("./data_/test_out.png", "wb") as f:
        f.write(result)