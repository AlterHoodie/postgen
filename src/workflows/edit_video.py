import uuid
import os
from pathlib import Path

from PIL import Image, ImageDraw
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

from src.prompts import HTML_TEMPLATE_OVERLAY_TEXT
from src.utils import convert_simple_text_to_html, capture_html_screenshot, cleanup_files


def create_gradient_overlay(width, height, gradient_height_ratio=0.35):
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


def create_overlay_image(headline, subtext, session_id):
    """
    Create the overlay image with text using HTML template
    """
    # Convert simple text to styled HTML
    headline_html, subtext_html = convert_simple_text_to_html(headline, subtext)
    
    # Create HTML content using template
    if headline:
        html_content = HTML_TEMPLATE_OVERLAY_TEXT.format(
            headline=headline_html,
            sub_text=subtext_html
        )
    else:
        html_content = HTML_TEMPLATE_OVERLAY_TEXT.format(
            headline="",
            sub_text=subtext_html
        )
    
    # Save HTML template
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


def process_overlay_for_transparency(input_path, output_path, target_width=576, target_height=720):
    """
    Process overlay image to make black areas transparent
    """
    try:
        img = Image.open(input_path).convert("RGBA")
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return False
    
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
    resized_img.save(output_path, "PNG")
    print(f"Processed overlay image: {output_path}")
    return True


def create_final_video(video_path, overlay_image_path, output_path, add_gradient=True, 
                      target_width=576, target_height=720):
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
            gradient_path = f"./data_/gradient_{uuid.uuid4().hex[:8]}.png"
            gradient_img.save(gradient_path, "PNG")
            
            gradient_clip = ImageClip(gradient_path).with_duration(final_clip.duration)
            clips_to_composite.append(gradient_clip)
            print(f"Added black gradient to bottom 35% of video")
        else:
            gradient_path = None
        
        # Process overlay image to match target dimensions
        overlay_img = Image.open(overlay_image_path)
        overlay_resized = overlay_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        overlay_resized_path = f"./data_/overlay_resized_{uuid.uuid4().hex[:8]}.png"
        overlay_resized.save(overlay_resized_path, "PNG")
        
        overlay_clip = ImageClip(overlay_resized_path)
        overlay_clip = overlay_clip.with_duration(final_clip.duration)
        clips_to_composite.append(overlay_clip.with_position("center"))
        
        # Composite all clips together
        final_composite = CompositeVideoClip(clips_to_composite)
        
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


def workflow(video_bytes, subtext, headline=""):
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
            headline=headline, 
            subtext=subtext, 
            session_id=session_id,
        )
        temp_files.extend([overlay_image_path, html_path])
        
        processed_overlay_path = f"./data/scoopwhoop/temp/processed_overlay_{session_id}.png"
        success = process_overlay_for_transparency(
            input_path=overlay_image_path,
            output_path=processed_overlay_path,
            target_width=576,
            target_height=720
        )
        
        if not success:
            print("Failed to process overlay image")
            return None
            
        temp_files.append(processed_overlay_path)
        
        # Step 4: Create the final video (576x720)
        output_video_path = f"./data/scoopwhoop/temp/final_video_{session_id}.mp4"
        final_video_path, video_temp_files = create_final_video(
            video_path=input_video_path,
            overlay_image_path=processed_overlay_path,
            output_path=output_video_path,
            add_gradient=True,
            target_width=576,
            target_height=720
        )
        temp_files.extend(video_temp_files)
        
        if not final_video_path:
            print("Failed to create final video")
            return None
        
        print(f"Workflow completed successfully: {final_video_path}")
        with open(final_video_path, "rb") as f:
            temp_files.append(final_video_path)
            return f.read()
        
    except Exception as e:
        print(f"Error in workflow: {e}")
        return None
        
    finally:
        # Step 5: Clean up temp files
        cleanup_files(temp_files)
        print(f"Cleaned up {len(temp_files)} temporary files")


# Test function for development
if __name__ == "__main__":
    # Test the workflow
    with open("./data_/2.mp4", "rb") as f:
        video_bytes = f.read()
    
    result = workflow(
        video_bytes=video_bytes,
        subtext="No more snail mail—India Post goes digital. A smarter era begins."
    )
    with open("./data_/final_video.mp4", "wb") as f:
        f.write(result)
    if result:
        print(f"✅ Success! Final video: ./data_/final_video.mp4")
    else:
        print("❌ Failed to create video")