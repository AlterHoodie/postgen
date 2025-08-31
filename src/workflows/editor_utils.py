import re
from typing import Tuple

from PIL import Image
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

from src.utils import (
    capture_html_screenshot,
    create_gradient_overlay,
)

def create_overlay_image(
    text: dict, assets: dict, html_template: str, session_id: str, page_name: str, get_video: bool = False, class_name:str = ""
) -> Tuple[str, str]:
    """
    Create the overlay image with text using HTML template
    """
    # Save HTML template
    html_content = html_template.format(**text, **assets)
    html_path = f"./data/{page_name}/temp/temp_overlay_{session_id}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # Create overlay image from HTML
    overlay_image_path = f"./data/{page_name}/temp/overlay_{session_id}.png"
    video_rect = capture_html_screenshot(
        file_path=html_path,
        element_selector=".container",
        output=overlay_image_path,
        get_video=get_video,
        class_name=class_name,
    )

    return overlay_image_path, html_path, video_rect


def create_image_over_video(
    video_path: str,
    overlay_image_path: str,
    page_name: str,
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
            gradient_path = f"./data/{page_name}/temp/gradient_{session_id}.png"
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
            f"./data/{page_name}/temp/overlay_resized_{session_id}.png"
        )
        overlay_resized.save(overlay_resized_path, "PNG")

        overlay_clip = ImageClip(overlay_resized_path)
        overlay_clip = overlay_clip.with_duration(final_clip.duration)
        clips_to_composite.append(overlay_clip.with_position("center"))

        # Composite all clips together
        final_composite = CompositeVideoClip(clips_to_composite)
        output_path = f"./data/{page_name}/temp/final_video_{session_id}.mp4"

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
        return None, []


def create_video_over_image(image_path:str, page_name:str, video_path:str, session_id:str, max_scale:float = 0.8, duration:float = None, width:int = 0, height:int = 0, x:int = 0, y:int = 0, padding:int = 0) -> Tuple[str, str]:
    """
    Create a video with a background image and a video overlay
    Uses Selenium coordinates to position video with CSS-like styling (width: 100%, height: 80%, object-fit: cover)
    """
    try:
        # Load the background image
        background = ImageClip(image_path)
        bg_width, bg_height = background.size

        # Load the video to overlay
        video_clip = VideoFileClip(video_path)
        original_width, original_height = video_clip.size

        if width and height:
            # Use the exact dimensions from Selenium (which represent the CSS-styled area)
            target_width = width
            target_height = height

            # Calculate aspect ratios for object-fit: cover behavior
            target_ratio = target_width / target_height
            original_ratio = original_width / original_height

            # Apply object-fit: cover behavior - crop to fill the area completely
            if original_ratio > target_ratio:
                # Video is wider - crop width to fit target ratio
                crop_height = original_height
                crop_width = int(crop_height * target_ratio)

                # Crop from center
                cropped_clip = video_clip.cropped(
                    width=crop_width,
                    height=crop_height,
                    x_center=original_width / 2,
                    y_center=original_height / 2,
                )
            else:
                # Video is taller - crop height to fit target ratio
                crop_width = original_width
                crop_height = int(crop_width / target_ratio)

                # Crop from center
                cropped_clip = video_clip.cropped(
                    width=crop_width,
                    height=crop_height,
                    x_center=original_width / 2,
                    y_center=original_height / 2,
                )
    
            # Resize to exact target dimensions (from Selenium)
            final_clip = cropped_clip.resized((target_width, target_height))
        else:   
            # Fallback: Use padding to preserve aspect ratio
            scale_w = width / original_width if width > 0 else 1
            scale_h = height / original_height if height > 0 else 1
            scale = min(scale_w, scale_h) * max_scale  # Apply max_scale
            
            # Resize video maintaining aspect ratio
            resized_clip = video_clip.resized(scale)
            
            # Create final video with black padding
            x_pos = (width - resized_clip.w) // 2 if width > 0 else 0
            y_pos = (height - resized_clip.h) // 2 if height > 0 else 0
            
            final_clip = CompositeVideoClip(
                [resized_clip.with_position((x_pos, y_pos))], 
                size=(width if width > 0 else resized_clip.w, height if height > 0 else resized_clip.h),
                bg_color=(0, 0, 0)
            )

        # Create composite video with background
        background = background.with_duration(final_clip.duration)
        
        # Position the video using Selenium coordinates
        if x and y:
            # Use exact Selenium coordinates for positioning
            final_video = CompositeVideoClip([background, final_clip.with_position((x - (width - padding)//2 , y))])
        else:
            # Center the video if no coordinates provided
            final_video = CompositeVideoClip([background, final_clip.with_position("center")])

        # Write the result
        output_path = f"./data/{page_name}/temp/final_video_{session_id}.mp4"
        final_video.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            fps=20,
            preset="medium",
            bitrate="2500k",
            audio_bitrate="128k",
            logger=None
            )

        # Clean up
        background.close()
        video_clip.close()
        final_video.close()

        return output_path, [image_path, video_path]
    except Exception as e:
        print(f"Error during video processing: {e}")
        return None, []