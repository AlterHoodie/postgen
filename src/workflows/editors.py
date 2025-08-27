import logging
import uuid
from pathlib import Path
from typing import Tuple
import re

from PIL import Image
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

from src.utils import (
    capture_html_screenshot,
    cleanup_files,
    convert_text_to_html,
    create_gradient_overlay,
    process_overlay_for_transparency,
)

logger = logging.getLogger(__name__)


def image_editor(text: dict, assets: dict, image_edits: dict, html_template: str, session_id: str) -> bytes:
    try:
        if html_template is None:
            raise ValueError("HTML template is None")
        if text is None:
            raise ValueError("Text template is None")
        
        temp_dir = Path("./data/scoopwhoop/temp")
        temp_dir.mkdir(exist_ok=True)
        temp_files = []

        # Check if this is a text-based template 
        html_content = html_template.format(**assets, **image_edits, **text)

        html_path = f"./data/scoopwhoop/temp/temp_overlay_{session_id}.html"
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


def _create_overlay_image(
    text: dict, assets: dict, html_template: str, session_id: str
) -> Tuple[str, str]:
    """
    Create the overlay image with text using HTML template
    """
    # Save HTML template
    html_content = html_template.format(**text, **assets)
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


def _create_image_over_video(
    video_path: str,
    overlay_image_path: str,
    session_id: str,
    target_width: int = 1080,
    target_height: int = 1350,
    offset: int = 0,
    add_gradient: bool = True,
    crop_type: str = "cover",
) -> Tuple[bytes, str]:
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
        if crop_type == "cover":
            cropped_clip = video_clip.cropped(
                width=crop_width,
                height=crop_height,
                x_center=original_width / 2,
                y_center=original_height / 2,
            )
            final_clip = cropped_clip.resized((target_width, target_height))
        else:   
            # Use padding to preserve aspect ratio
            scale_w = target_width / original_width
            scale_h = target_height / original_height
            scale = min(scale_w, scale_h)  # Use smaller scale to fit within bounds
            
            # Resize video maintaining aspect ratio
            resized_clip = video_clip.resized(scale)
            
                        # Create final video with black padding (slightly below center)
            # Calculate position to be slightly down from center
            x_pos = (target_width - resized_clip.w) // 2  # Center horizontally
            y_pos = (target_height - resized_clip.h) // 2 + offset  # 30 pixels down from center
            
            final_clip = CompositeVideoClip([resized_clip.with_position((x_pos, y_pos))], size=(target_width, target_height),bg_color=(0, 0, 0))  
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
        overlay_resized = overlay_img.resize(
            (target_width, target_height), Image.Resampling.LANCZOS
        )
        overlay_resized_path = (
            f"./data/scoopwhoop/temp/overlay_resized_{session_id}.png"
        )
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
            codec="libx264",
            audio_codec="aac",
            threads=4,
            fps=20,
            preset="medium",
            bitrate="2500k",
            audio_bitrate="128k",
            logger=None,
        )

        # Close clips to free memory
        video_clip.close()
        final_composite.close()

        return output_path, [overlay_image_path, overlay_resized_path, gradient_path]

    except Exception as e:
        print(f"Error during video processing: {e}")
        return None


def _create_video_over_image(image_path:str, video_path:str, session_id:str, max_scale:float = 0.8, duration:float = None) -> Tuple[str, str]:
    """
    Create a video with a background image and a video overlay
    """
    # Load the background image
    background = ImageClip(image_path)
    bg_width, bg_height = background.size
    
    # Load the video to overlay
    video_clip = VideoFileClip(video_path)
    video_width, video_height = video_clip.size
    
    # Calculate appropriate size while maintaining aspect ratio
    # Scale video to fit within the background with some padding
    scale_x = (bg_width * max_scale) / video_width
    scale_y = (bg_height * max_scale) / video_height
    
    # Use the smaller scale to ensure video fits completely
    scale_factor = min(scale_x, scale_y)
    
    new_width = int(video_width * scale_factor)
    new_height = int(video_height * scale_factor)
    
    # Resize the video while maintaining aspect ratio
    video_clip = video_clip.resized((new_width, new_height))
    
    # Set duration (use video duration if not specified)
    if duration is None:
        duration = video_clip.duration
    
    # Set background duration to match
    background = background.with_duration(duration)
    
    # Center the video on the background
    video_clip = video_clip.with_position('center')
    
    # Create composite video
    final_video = CompositeVideoClip([background, video_clip])
    
    # Write the result
    output_path = f"./data/scoopwhoop/temp/final_video_{session_id}.mp4"
    final_video.write_videofile(output_path, 
                               codec='libx264', 
                               audio_codec='aac',
                               fps=video_clip.fps,
                               preset="medium",
                               bitrate="2500k",
                               audio_bitrate="128k",
                               logger=None)
    
    # Clean up
    background.close()
    video_clip.close()
    final_video.close()


def video_editor(text: dict,assets:dict ,video_edits: dict, html_template: str, session_id: str) -> bytes:
    """
    Complete workflow to create edited video with text overlay

    Args:
        video_bytes: Raw video file bytes
        headline: Main headline text
        subtext: Subtitle text

    Returns:
        str: Path to the final video file, or None if failed
    """
    temp_files = []

    try:
        # Create temp directory
        temp_dir = Path("./data/scoopwhoop")
        temp_dir.mkdir(exist_ok=True)
        temp_files.extend([value for key, value in assets.items()])
        video_src = assets.get("background_video")
        del assets['background_video']

        # Step 2: Create the overlay image with text
        overlay_image_path, html_path = _create_overlay_image(
            text=text,
            assets=assets,
            html_template=html_template,
            session_id=session_id,
        )
        temp_files.extend([overlay_image_path, html_path])
        if video_edits.get("type") == "image_overlay":
            processed_overlay_path = process_overlay_for_transparency(
                image_path=overlay_image_path,
                session_id=session_id,
                target_width=1080,
                target_height=1350,
            )
            # Step 4: Create the final video (576x720)
            final_video_path, video_temp_files = _create_image_over_video(
                video_path=video_src,
                overlay_image_path=processed_overlay_path,
                session_id=session_id,
                add_gradient=video_edits.get("add_gradient", True),
                target_width=1080,
                target_height=1350,
                crop_type=video_edits.get("crop_type", "cover"),
                offset=video_edits.get("offset", 0),
            )
            temp_files.append(processed_overlay_path)
        else:
            final_video_path, video_temp_files = _create_video_over_image(
                image_path=overlay_image_path,
                video_path=video_src,
                session_id=session_id,
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


def text_editor(
    template: dict,
    image_edits: dict,
    video_edits: dict,
    text: dict,
    assets: dict,
    session_id: str,
    is_video: bool = False,
) -> bytes:
    """
    Editor for text-based templates
    """
    html_template = template["overlay_template"] if is_video else template["html_template"]

    # Process text inputs
    text_input = {}
    text_template = template["text"]
    
    # Add defaults for missing keys
    for key, value in text_template.items():
        if key not in text and "default" in value:
            text_input[key] = value["default"]
    
    # Process provided text values
    for key, value in text.items():
        if key not in text_template:
            continue
        
        template_config = text_template[key]
        if template_config["type"] in ["text", "text_area"]:
            text_input[key] = convert_text_to_html(
                tag=template_config["tag"],
                class_name=template_config["class"],
                text=value,
            )
        elif template_config["type"] == "checkbox":
            text_input[key] = template_config["html_snippet"] if value else ""
        elif template_config["type"] == "dropdown":
            text_input[key] = value

    # Process assets
    assets_input = assets
    assets_template = template["assets"]
    
    # Add defaults for missing assets
    for key, value in assets_template.items():
        if key not in assets and "default" in value:
            assets_input[key] = value["default"]

    # Process edits based on video/image mode
    if is_video:
        edits_template = template["video_edits"]
        edits_input = video_edits
    else:
        edits_template = template["image_edits"]
        edits_input = image_edits

    # Process edits
    processed_edits = {}
    for key, value in edits_template.items():
        if key not in edits_input and "default" in value:
            processed_edits[key] = value["default"]
    
    for key, value in edits_input.items():
        if key in edits_template and edits_template[key]["type"] in ["default", "dropdown"]:
            processed_edits[key] = value

    # Call appropriate editor
    if is_video:
        return video_editor(
            text=text_input,
            assets=assets_input,
            video_edits=processed_edits,
            html_template=html_template,
            session_id=session_id,
        )
    else:
        return image_editor(
            text=text_input,
            assets=assets_input,
            image_edits=processed_edits,
            html_template=html_template,
            session_id=session_id,
        )


# Test function for development
if __name__ == "__main__":
    from src.templates.scoopwhoop.thumbnail import thumbnail_template
    ## Test Image Workflow
    final_image = text_editor(
        template=thumbnail_template['slides']['headline_slide'],
        image_edits={"crop_type": "cover"},
        video_edits={},
        text={"headline": "**IPL just doesn't** seem that exciting anymore.",
              "subtext": "The IPL is a cricket tournament that is played in India. It is a very popular tournament and is watched by millions of people all over the world.",
              "is_trigger": True,
              "source":"Source: IPL"},
        assets={"background_image": "test.png"},
        is_video=False,
        session_id="test",
    )

    with open("./data_/test_out.png", "wb") as f:
        f.write(final_image)