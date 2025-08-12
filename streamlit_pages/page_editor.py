import streamlit as st
import os
import io
from typing import Dict, Tuple
from PIL import Image
from src.workflows.editors import text_editor
from src.utils import extract_text_from_html
from src.templates import get_template_config


def text_editor_form(
    text_values: Dict,
    content_bytes: bytes,
    template: Dict,
    slide_name: str,
    form_key: str,
    is_video: bool = False,
) -> Tuple[bytes, bool]:
    """
    Simple Streamlit form for text editing using text_editor from editors.py

    Args:
        text_json: Text template configuration
        image_bytes: Original image bytes
        template: Template configuration
        slide_name: Slide name
        form_key: Unique form key

    Returns:
        (new_image_bytes, submitted)
    """
    text_json = template["slides"][slide_name]["text_json"]
    with st.form(key=form_key):
        text_input = {}
        st.info("Use \*\*<text>\*\* for highlighting text in Yellow.")
        # Create inputs based on text_json
        for field_name, config in text_json.get("text_template", {}).items():
            display_name = field_name.replace("_", " ").title()

            if config.get("type") == "checkbox":
                text_input[field_name] = st.checkbox(
                    display_name, value=True if text_values.get(field_name,"") else False
                )
            elif config.get("type") == "text_area":
                text_input[field_name] = st.text_area(
                    f"{display_name}:",
                    value=extract_text_from_html(text_values.get(field_name,"")),
                )
            elif config.get("type") == "text":
                text_input[field_name] = st.text_area(
                    f"{display_name}:",
                    value=extract_text_from_html(text_values.get(field_name,"")),
                )

        submitted = st.form_submit_button("Generate New Image", type="primary")

        if submitted:
            try:
                if is_video:
                    new_image_bytes = text_editor(
                        template, slide_name, text_input, content_bytes, is_video=True
                    )
                else:
                    new_image_bytes = text_editor(
                        template, slide_name, text_input, content_bytes
                    )
                return new_image_bytes, True
            except Exception as e:
                st.error(f"Error: {e}")
                return None, False

        return None, False


def show_post_editor_page():
    """Simple post editor with image/video upload, template selection, and slide editing"""
    st.title("✏️ Post Editor")
    st.markdown("Create posts with your own images/videos")
    
    # Add tabs for different editor types
    tab1, tab2 = st.tabs(["📷 Image/Video Editor", "📝 Text-Only Editor"])
    
    with tab1:
        show_media_editor()
    
    with tab2:
        show_text_only_editor()


def show_media_editor():
    """Media editor for image/video uploads"""
    # Step 1: Upload Media
    uploaded_file = st.file_uploader(
        "Choose an image or video file",
        type=["png", "jpg", "jpeg", "gif", "mp4", "mov", "avi"],
        help="Supported formats: PNG, JPG, JPEG, GIF, MP4, MOV, AVI",
    )

    if uploaded_file is None:
        st.info("👆 Please upload an image or video to get started")
        return

    # Show uploaded file
    file_type = get_file_type(uploaded_file.name)
    
    # Validate uploaded file
    try:
        file_bytes = uploaded_file.getvalue()
        if not file_bytes:
            st.error("Uploaded file is empty")
            return
        
        # For images, try to validate with PIL
        if file_type == "image":
            from PIL import Image
            try:
                # Test if image can be opened
                test_img = Image.open(io.BytesIO(file_bytes))
                test_img.verify()  # Verify image integrity
                uploaded_file.seek(0)  # Reset file pointer
            except Exception as img_error:
                st.error(f"Invalid image file: {img_error}")
                return
                
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")
        return

    template_options = {
        "Timeline": "timeline",
        "Writeup": "writeup",
        "Thumbnail": "thumbnail",
    }

    # Step 3: Slide Selection and Editing
    selected_template = st.selectbox(
        "Choose template:",
        options=list(template_options.keys()),
        help="Choose the template style for your content",
    )

    template_key = template_options[selected_template]
    template_config = get_template_config(template_key)


    slides = list(template_config["slides"].keys())
    selected_slide = st.selectbox(
        "Choose slide to edit:",
        slides,
        format_func=lambda x: x.replace("_", " ").title(),
    )

    # Check if a new file was uploaded (different from previous)
    current_file_info = f"{uploaded_file.name}_{len(file_bytes)}_{file_type}"
    if "current_file_info" not in st.session_state:
        st.session_state.current_file_info = current_file_info
    elif st.session_state.current_file_info != current_file_info:
        # New file uploaded - clear all slide data
        st.session_state.slide_data = {}
        st.session_state.current_file_info = current_file_info

    # Initialize slide data in session state
    if "slide_data" not in st.session_state:
        st.session_state.slide_data = {}
    if selected_slide not in st.session_state.slide_data:
        st.session_state.slide_data[selected_slide] = initialize_slide_fields(
            template_config["slides"][selected_slide]
        )

    # Edit current slide
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Edit Content:**")

        media_bytes = uploaded_file.getvalue()
        is_video = file_type == "video"

        new_content_bytes, submitted = text_editor_form(
            text_values=st.session_state.slide_data[selected_slide],
            content_bytes=media_bytes,
            template=template_config,
            slide_name=selected_slide,
            form_key=f"edit_{selected_slide}",
            is_video=is_video,
        )

        if submitted and new_content_bytes:
            st.session_state.slide_data[selected_slide][
                "edited_content"
            ] = new_content_bytes
            st.success("✅ Slide updated!")

    with col2:
        st.markdown("**Preview:**")

        if "edited_content" in st.session_state.slide_data[selected_slide]:
            content_bytes = st.session_state.slide_data[selected_slide][
                "edited_content"
            ]

            if is_video:
                st.video(content_bytes, width=500)
            else:
                st.image(content_bytes, width=500)

            # Download button
            file_ext = "mp4" if is_video else "png"
            filename = f"{selected_slide}.{file_ext}"

            st.download_button(
                label="📥 Download",
                data=content_bytes,
                file_name=filename,
                mime=f"{'video' if is_video else 'image'}/{file_ext}",
                use_container_width=True,
            )
        else:
            if is_video:
                st.video(media_bytes, width=500)
                st.caption("Original video")
            else:
                st.image(media_bytes, width=500)
                st.caption("Original image")


def get_file_type(filename: str) -> str:
    """Determine if file is image or video based on extension"""
    image_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    video_extensions = [".mp4", ".mov", ".avi"]

    ext = os.path.splitext(filename.lower())[1]

    if ext in image_extensions:
        return "image"
    elif ext in video_extensions:
        return "video"
    else:
        return "unknown"


def initialize_slide_fields(slide_config: Dict) -> Dict:
    """Initialize fields for a single slide"""
    fields = {}

    if "text_json" in slide_config and "text_template" in slide_config["text_json"]:
        for field_name, field_config in slide_config["text_json"][
            "text_template"
        ].items():
            if field_config.get("type") == "checkbox":
                fields[field_name] = False
            else:
                fields[field_name] = ""

    return fields


def show_text_only_editor():
    """Simple text-only editor for templates that don't need uploaded images"""
    
    # Template selection - only text_based for now
    text_only_template_config = get_template_config("text_based")
    
    # Get the slide (text_based only has one slide)
    slide_name = "text_based_slide"
    
    # Initialize session state for text-only editor
    if "text_only_data" not in st.session_state:
        st.session_state.text_only_data = initialize_slide_fields(
            text_only_template_config["slides"][slide_name]
        )
    
    # Create the form
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Create Text-Based Post:**")
        
        # Create a simple form for text-based template
        with st.form(key="text_only_form"):
            text_input = {}
            st.info("Use \*\*<text>\*\* for highlighting text in Yellow.")
            
            # Get text template config
            text_json = text_only_template_config["slides"][slide_name]["text_json"]
            
            for field_name, config in text_json.get("text_template", {}).items():
                display_name = field_name.replace("_", " ").title()
                
                if config.get("type") == "dropdown":
                    text_input[field_name] = st.selectbox(
                        f"{display_name}:",
                        options=config.get("values", []),
                        index=0 if config.get("values") else 0
                    )
                elif config.get("type") == "text_area":
                    text_input[field_name] = st.text_area(
                        f"{display_name}:",
                        value=st.session_state.text_only_data.get(field_name, ""),
                        help="Use <span class=\"yellow\">text</span> for highlighting"
                    )
                elif config.get("type") == "text":
                    text_input[field_name] = st.text_input(
                        f"{display_name}:",
                        value=st.session_state.text_only_data.get(field_name, ""),
                        help="Use <span class=\"yellow\">text</span> for highlighting"
                    )
                elif config.get("type") == "dropdown":
                    text_input[field_name] = st.selectbox(
                        f"{display_name}:",
                        options=config.get("values", []),
                        index=0 if config.get("values") else 0
                    )
            
            submitted = st.form_submit_button("Generate Image", type="primary")
            
            if submitted:
                try:
                    # Generate the image using text_editor
                    new_image_bytes = text_editor(
                        text_only_template_config, slide_name, text_input
                    )
                    
                    if new_image_bytes:
                        st.session_state.text_only_data.update(text_input)
                        st.session_state.text_only_data["generated_image"] = new_image_bytes
                        st.success("✅ Image generated!")
                    else:
                        st.error("Failed to generate image")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        st.markdown("**Preview:**")
        
        if "generated_image" in st.session_state.text_only_data:
            image_bytes = st.session_state.text_only_data["generated_image"]
            st.image(image_bytes, width=500)
            
            # Download button
            st.download_button(
                label="📥 Download Image",
                data=image_bytes,
                file_name="text_based_post.png",
                mime="image/png",
                use_container_width=True,
            )
        else:
            st.info("👆 Fill out the form and click 'Generate Image' to see preview")
