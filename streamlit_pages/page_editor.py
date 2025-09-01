import streamlit as st
import io
import uuid
from typing import Dict, Tuple

from PIL import Image

from src.workflows.editors import text_editor
from src.utils import extract_text_from_html, get_file_type
from src.templates import get_template_config


def text_editor_form(
    text_values: Dict,
    template: Dict,
    slide_name: str,
    form_key: str,
    page_name: str,
    content_bytes: bytes,
    show_image_upload: bool = False,
    is_video: bool = False,
    session_id: str = None,
) -> Tuple[bytes, bool]:
    """
    Dynamic Streamlit form generator that handles all template configurations
    including text fields, assets, dropdowns, checkboxes, and file uploads

    Args:
        text_values: Current text values
        content_bytes: Original image/video bytes
        template: Template configuration
        slide_name: Slide name
        form_key: Unique form key
        page_name: Page name (e.g., 'scoopwhoop', 'twitter')
        is_video: Whether content is video
        show_image_upload: Whether to show image upload option
        session_id: Session ID for file naming

    Returns:
        (new_content_bytes, submitted)
    """
    slide_config = template["slides"][slide_name]
    with st.form(key=form_key):
        text_input = {}
        assets_input = {}
        image_edits_input = {}
        video_edits_input = {}
        custom_content_bytes = content_bytes
        if show_image_upload:
            uploaded_image = st.file_uploader(
                "Dont like the background? Upload your own background image",
                type=["png", "jpg", "jpeg"],
                help="If you upload an image, it will be used instead of the generated background",
                key=f"{form_key}_image_upload"
            )
            
            # Choose which image to use
            use_uploaded = uploaded_image is not None
            if use_uploaded:
                try:
                    custom_content_bytes = uploaded_image.getvalue()
                except Exception as e:
                    st.error(f"Error reading uploaded image: {e}")
                    use_uploaded = False
                    custom_content_bytes = content_bytes
            else:
                custom_content_bytes = content_bytes
            
            st.markdown("---")
        # Create inputs for text fields
        st.subheader("Text Content")
        text_fields = slide_config["text"]
                
        for field_name, config in text_fields.items():
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
                    text_input[field_name] = st.text_input(
                        f"{display_name}:",
                        value=extract_text_from_html(text_values.get(field_name,"")),
                    )
                elif config.get("type") == "dropdown":
                    current_value = text_values.get(field_name, config.get("default", ""))
                    options = config.get("values", [])
                    default_index = 0
                    if current_value in options:
                        default_index = options.index(current_value)
                    text_input[field_name] = st.selectbox(
                        f"{display_name}:",
                        options=options,
                        index=default_index
                    )

        if is_video:
            assets_input["background_video"] = {"file_type": "bytes", "content": custom_content_bytes, "extension": "mp4"}
        else:
            assets_input["background_image"] = {"file_type": "bytes", "content": custom_content_bytes, "extension": "png"}

        if "assets" in slide_config:
            for field_name, config in slide_config["assets"].items():
                if field_name in ["background_image","background_video"]:
                    continue
                display_name = field_name.replace("_", " ").title()
                if config.get("type") == "dropdown":
                    options = config.get("values", [])
                    default_value = config.get("default", options[0] if options else "")
                    value = st.selectbox(
                        f"{display_name}:",
                        options=options,
                        index=options.index(default_value) if default_value in options else 0
                    )
                    assets_input[field_name] = {"file_type": "path", "content": value}
                elif config.get("type") == "bytes":
                    value = st.file_uploader(
                        f"{display_name}:",
                        type=config.get("file_type", ""),
                        help=config.get("help", "")
                    )
                    if value is not None:
                        assets_input[field_name] = {"file_type": "bytes", "content": value.getvalue(), "extension": get_file_type(value.name)}

            
        # Create inputs for image/video edits
        if is_video and "video_edits" in slide_config:
            st.subheader("Video Settings")
            for field_name, config in slide_config["video_edits"].items():
                display_name = field_name.replace("_", " ").title()
                if config.get("type") == "dropdown":
                    options = config.get("values", [])
                    default_value = config.get("default", options[0] if options else "")
                    video_edits_input[field_name] = st.selectbox(
                        f"{display_name}:",
                        options=options,
                        index=options.index(default_value) if default_value in options else 0
                    )
                elif config.get("type") == "default":
                    video_edits_input[field_name] = config.get("values", "")
                
        elif not is_video and "image_edits" in slide_config and slide_config["image_edits"]:
            st.subheader("Image Settings")
            for field_name, config in slide_config["image_edits"].items():
                display_name = field_name.replace("_", " ").title()
                if config.get("type") == "dropdown":
                    options = config.get("values", [])
                    default_value = config.get("default", options[0] if options else "")
                    image_edits_input[field_name] = st.selectbox(
                        f"{display_name}:",
                        options=options,
                        index=options.index(default_value) if default_value in options else 0
                    )
                elif config.get("type") == "default":
                    image_edits_input[field_name] = config.get("default", "")

        submitted = st.form_submit_button("Generate New Video" if is_video else "Generate New Image", type="primary")
        st.info("Use \*\*<text>\*\* for highlighting text in Yellow.")

        if submitted:
            try:
                if session_id is None:
                    session_id = str(uuid.uuid4())[:8]

                for key, value in assets_input.items():
                    if value.get("file_type") == "bytes":
                        file_name = f"{key}_{session_id}.{value.get('extension')}"
                        file_path = f"./data/{page_name}/temp/{file_name}"
                        with open(file_path, "wb") as f:
                            f.write(value.get("content"))
                        assets_input[key] = file_path
                    elif value.get("file_type") == "path":
                        assets_input[key] = value.get("content")
                
                new_content_bytes = text_editor(
                    template=slide_config,
                    page_name=page_name,
                    image_edits=image_edits_input,
                    video_edits=video_edits_input,
                    text=text_input,
                    assets=assets_input,
                    session_id=session_id,
                    is_video=is_video
                )
                return new_content_bytes, True
            except Exception as e:
                st.error(f"Error: {e}")
                return None, False

        return None, False

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

    # Page selection
    page_name = st.selectbox(
        "Select page:",
        ["scoopwhoop", "twitter", "social_village", "infomance"],
        help="Choose which page/brand to create content for"
    )
    
    # Template options based on page
    if page_name == "scoopwhoop":
        template_options = {
            "Timeline": "timeline",
            "Writeup": "writeup",
            "Thumbnail": "thumbnail",
            "Meme": "meme",
        }
    elif page_name == "twitter":
        template_options = {
            "Tweet Image": "tweet_image",
        }
    elif page_name == "social_village":
        template_options = {
            "Content": "content",
            "Thumbnail": "thumbnail"
        }
    elif page_name == "infomance":
        template_options = {
            "Content": "content",
            "Thumbnail": "thumbnail"
        }
    else:
        template_options = {}

    # Step 3: Slide Selection and Editing
    selected_template = st.selectbox(
        "Choose template:",
        options=list(template_options.keys()),
        help="Choose the template style for your content",
    )

    template_key = template_options[selected_template]
    template_config = get_template_config(template_key, page_name)


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
            page_name=page_name,
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

def show_text_only_editor():
    """Simple text-only editor for templates that don't need uploaded images"""
    
    # Page and template selection
    page_name = st.selectbox(
        "Select page:",
        ["scoopwhoop", "the_sarcastic_indian","twitter"],
        help="Choose which page/brand to create content for"
    )
    
    # Template selection - only text_based for now
    text_only_template_config = get_template_config("text_based", page_name)
    
    # Get the slide (text_based only has one slide)
    slide_name = "text_based_slide"
    
    # Initialize session state for text-only editor
    if "text_only_data" not in st.session_state:
        st.session_state.text_only_data = initialize_slide_fields(
            text_only_template_config["slides"][slide_name]
        )
    if "text_only_page" not in st.session_state:
        st.session_state.text_only_page = page_name
    elif st.session_state.text_only_page != page_name:
        # Page changed, reset data
        st.session_state.text_only_data = initialize_slide_fields(
            text_only_template_config["slides"][slide_name]
        )
        st.session_state.text_only_page = page_name
    
    # Create the form
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Create Text-Based Post:**")
        
        # Create a simple form for text-based template
        with st.form(key="text_only_form"):
            text_input = {}
            assets_input = {}
            image_edits_input = {}
            st.info("Use \*\*<text>\*\* for highlighting text in Yellow.")
            
            # Get slide config
            slide_config = text_only_template_config["slides"][slide_name]
            
            text_fields = slide_config["text"]                    
            for field_name, config in text_fields.items():
                    display_name = field_name.replace("_", " ").title()
                    if config.get("type") == "dropdown":
                        current_value = st.session_state.text_only_data.get(field_name, config.get("default", ""))
                        options = config.get("values", [])
                        default_index = 0
                        if current_value in options:
                            default_index = options.index(current_value)
                        text_input[field_name] = st.selectbox(
                            f"{display_name}:",
                            options=options,
                            index=default_index
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
                    elif config.get("type") == "checkbox":
                        text_input[field_name] = st.checkbox(
                            display_name,
                            value=st.session_state.text_only_data.get(field_name, False)
                        )
            
            # Assets inputs (if any)
            if "assets" in slide_config:
                for field_name, config in slide_config["assets"].items():
                    display_name = field_name.replace("_", " ").title()
                    if config.get("type") == "dropdown":
                        options = config.get("values", [])
                        default_value = config.get("default", options[0] if options else "")
                        value = st.selectbox(
                            f"{display_name}:",
                            options=options,
                            index=options.index(default_value) if default_value in options else 0
                        )
                        assets_input[field_name] = {"file_type": "path", "content": value}
                    elif config.get("type") == "bytes":
                        value = st.file_uploader(
                            f"{display_name}:",
                            type=config.get("file_type", ""),
                            help=config.get("help", "")
                        )
                        if value is not None:
                            assets_input[field_name] = {"file_type": "bytes", "content": value.getvalue(), "extension": get_file_type(value.name)}
            
            # Image edits (if any)
            if "image_edits" in slide_config:
                for field_name, config in slide_config["image_edits"].items():
                    if config.get("type") == "dropdown":
                        display_name = field_name.replace("_", " ").title()
                        options = config.get("values", [])
                        default_value = config.get("default", options[0] if options else "")
                        image_edits_input[field_name] = st.selectbox(
                            f"{display_name}:",
                            options=options,
                            index=options.index(default_value) if default_value in options else 0
                        )
            submitted = st.form_submit_button("Generate Image", type="primary")
            
            if submitted:
                try:
                    # Generate the image using text_editor
                    session_id = str(uuid.uuid4())
                    for key, value in assets_input.items():
                        if value.get("file_type") == "bytes":
                            file_name = f"{key}_{session_id}.{value.get('extension')}"
                            file_path = f"./data/{page_name}/temp/{file_name}"
                            with open(file_path, "wb") as f:
                                f.write(value.get("content"))
                            assets_input[key] = file_path
                        elif value.get("file_type") == "path":
                            assets_input[key] = value.get("content")
                    new_image_bytes = text_editor(
                        template=slide_config,
                        page_name=page_name,
                        image_edits=image_edits_input,
                        video_edits={},
                        text=text_input,
                        assets=assets_input,
                        session_id=session_id,
                        is_video=False
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

def initialize_slide_fields(slide_config: Dict) -> Dict:
    """Initialize fields for a single slide"""
    fields = {}

    # Initialize text fields
    text_fields = {}
    if "text" in slide_config:
        # Handle nested text_template structure
        if "text_template" in slide_config["text"]:
            text_fields = slide_config["text"]["text_template"]
        else:
            text_fields = slide_config["text"]
    
    for field_name, field_config in text_fields.items():
        if field_config.get("type") == "checkbox":
            fields[field_name] = False
        elif field_config.get("type") == "dropdown":
            fields[field_name] = field_config.get("default", "")
        else:
            fields[field_name] = ""

    return fields