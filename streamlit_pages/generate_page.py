import streamlit as st
import asyncio
import time
import base64
import uuid
import concurrent.futures

from src.services.mongo_client import get_mongo_client
from src.templates import get_template_config
from src.workflows.content_creator import workflow
from streamlit_pages.page_editor import text_editor_form


def show_generate_page():
    st.title("🎨 Generate Content Slides")
    st.markdown("Enter a headline to generate content slides with images")

    # Page selection
    page_name = st.selectbox(
        "Select Page/Brand:",
        ["scoopwhoop", "twitter", "social_village", "infomance", "the_sarcastic_indian"],
        help="Choose which page/brand to create content for"
    )
    
    # Template options based on page
    if page_name == "scoopwhoop":
        template_options = {
            "Timeline": "timeline",
            "Thumbnail": "thumbnail",
            "Writeup": "writeup",
        }
    elif page_name == "twitter":
        template_options = {
            "Tweet Image": "tweet_image"
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
    elif page_name == "the_sarcastic_indian":
        template_options = {
            "Writeup": "writeup",
        }
    else:
        template_options = {}

    # Input for headline
    headline = st.text_input(
        "Enter Headline",
        placeholder="e.g., UttarKashi Cloud Burst India",
        help="Enter the headline for your content",
    )

    selected_template = st.selectbox(
        "Select Template",
        options=list(template_options.keys()),
        help="Choose the template style for your content",
    )

    if headline:
        col1, col2 = st.columns([1, 1])

        with col1:
            # Generate button
            if st.button(
                "🚀 Generate Content", type="primary", use_container_width=True
            ):
                generate_content(headline, template_options[selected_template], page_name)

        with col2:
            # Show latest results link
            if st.session_state.get("latest_session_id"):
                if st.button("📱 Show Latest Results", use_container_width=True):
                    st.session_state["show_results"] = True

    # Show results if available
    if st.session_state.get("show_results") and st.session_state.get(
        "latest_session_id"
    ):
        show_content_results(st.session_state["latest_session_id"])


def generate_content(headline: str, template_type: str, page_name: str):
    """Generate content slides with loading progress"""

    # Create progress tracking
    progress_container = st.empty()

    with progress_container.container():
        st.markdown("### 🔄 Generating Content...")
        progress_bar = st.progress(0)
        status_text = st.empty()

    try:
        # Get template configuration
        template = get_template_config(template_type, page_name)

        # Step 1: Initialize
        progress_bar.progress(20)
        status_text.text("📋 Creating story board...")
        time.sleep(1)

        # Step 2: Start workflow
        progress_bar.progress(40)
        status_text.text("🎨 Generating images...")

        # Run async workflow
        def run_workflow():
            return asyncio.run(
                workflow(headline=headline, template=template, save=True)
            )

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_workflow)
            session_id = future.result()

        # Step 3: Progress updates
        progress_bar.progress(80)
        status_text.text("📱 Finalizing slides...")
        time.sleep(1)

        # Step 4: Complete
        progress_bar.progress(100)
        status_text.text("✅ Content generated successfully!")

        # Store session_id and page_name in session state
        st.session_state["latest_session_id"] = session_id
        st.session_state["latest_page_name"] = page_name
        st.session_state["show_results"] = True

        time.sleep(1)
        st.rerun()

    except Exception as e:
        progress_bar.progress(0)
        st.error(f"❌ Error generating content: {str(e)}")
        status_text.text("Generation failed")

    finally:
        # Clear progress after 2 seconds
        time.sleep(2)
        progress_container.empty()


def show_content_results(session_id: str):
    """Display the generated content results with original image on left and slides dropdown on right"""
    try:
        # Fetch results from database
        result_key = f"content_result_{session_id}"

        if result_key not in st.session_state:
            mongo_client = get_mongo_client()
            result = mongo_client.get_workflow_result(session_id)
            mongo_client.close()
            st.session_state[result_key] = result
        else:
            result = st.session_state[result_key]

        if not result:
            st.error("No results found for this session")
            return

        st.markdown("---")
        st.markdown("### 📱 Generated Content Results")

        # Check if this is text-only content
        
        # Get slides data
        slides = result.get("slides", [])
        if not slides:
            st.warning("No slides found in results")
            return
        # Slide selection dropdown
        slide_options = [
            f"Slide {i+1}: {slide.get('name', f'slide_{i}')}"
            for i, slide in enumerate(slides)
        ]
        selected_slide_idx = st.selectbox(
            "Select a slide:",
            range(len(slide_options)),
            format_func=lambda i: slide_options[i],
        )
        is_text_only = slides[selected_slide_idx].get("image_description", "") == ""

        if is_text_only:
            show_text_only_results(session_id, result, slides, selected_slide_idx)
        else:
            show_media_results(session_id, result, slides, selected_slide_idx)

    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")


def show_text_only_results(session_id: str, result: dict, slides: list, selected_slide_idx: int):
    """Display text-only content results (no without_text overlay, only with_text)"""

    # Show selected slide details
    if selected_slide_idx is not None and selected_slide_idx < len(slides):
        selected_slide = slides[selected_slide_idx]

        # Show images
        slide_images = selected_slide.get("images", [])
        if slide_images:
            tab_names = [f"Image {i+1}" for i in range(len(slide_images))]
            tabs = st.tabs(tab_names)

            for tab_idx, (tab, img_data) in enumerate(zip(tabs, slide_images)):
                with tab:
                    # Show image type and model info
                    st.caption(
                        f"{img_data.get('type', 'unknown').title()} ({img_data.get('model', 'unknown')})"
                    )

                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("**Generated Image**")
                        # Check if there's an edited version in session state
                        edit_key = f"edited_{session_id}_{selected_slide_idx}_{tab_idx}"

                        if edit_key in st.session_state:
                            # Show edited image
                            st.image(st.session_state[edit_key], width=400)
                            st.download_button(
                                label="⬇️ Download Edited",
                                data=st.session_state[edit_key],
                                file_name=f"slide_{selected_slide_idx+1}_post_{tab_idx+1}_edited.png",
                                mime="image/png",
                                key=f"download_edited_{session_id}_{selected_slide_idx}_{tab_idx}",
                            )
                            

                            # Clear edit button
                            if st.button(
                                "🗑️ Clear Edit",
                                key=f"clear_{session_id}_{selected_slide_idx}_{tab_idx}",
                            ):
                                del st.session_state[edit_key]
                                st.rerun()
                        else:
                            # Show original with text
                            try:
                                # Validate base64 data exists
                                base64_data = img_data.get("images", {}).get("with_text", {}).get("image_base64")
                                if not base64_data:
                                    raise ValueError("No base64 image data found")
                                
                                with_text_data = base64.b64decode(base64_data)
                                if not with_text_data:
                                    raise ValueError("Decoded image data is empty")
                                
                                st.image(with_text_data, width=400)
                                st.download_button(
                                    label="⬇️ Download",
                                    data=with_text_data,
                                    file_name=f"slide_{selected_slide_idx+1}_post_{tab_idx+1}.png",
                                    mime="image/png",
                                    key=f"download_with_{session_id}_{selected_slide_idx}_{tab_idx}",
                                )
                            except Exception as e:
                                st.error(f"Failed to load image")

                    with col2:
                        # Text editor section
                        st.markdown("**Edit Text**")

                        # Get template and slide info for text editor
                        template_type = result.get("template_type", "writeup")
                        result_page_name = result.get("page_name", "the_sarcastic_indian")
                        template = get_template_config(template_type, result_page_name)
                        slide_name = selected_slide.get("name", "headline_slide")
                        
                        if "slides" in template and slide_name in template["slides"]:
                            try:
                                current_text_values = selected_slide.get("text_template", {})
                                
                                # Get the specific slide configuration
                                slide_config = template["slides"][slide_name]
                                
                                # Use text-only editor for editing
                                with st.form(key=f"text_edit_form_{session_id}_{selected_slide_idx}_{tab_idx}"):
                                    text_input = {}
                                    assets_input = {}
                                    
                                    # Text fields
                                    text_fields = slide_config["text"]
                                    for field_name, config in text_fields.items():
                                        display_name = field_name.replace("_", " ").title()
                                        if config.get("type") == "text_area":
                                            text_input[field_name] = st.text_area(
                                                f"{display_name}:",
                                                value=current_text_values.get(field_name, ""),
                                                help="Use **text** for highlighting"
                                            )
                                        elif config.get("type") == "text":
                                            text_input[field_name] = st.text_input(
                                                f"{display_name}:",
                                                value=current_text_values.get(field_name, ""),
                                                help="Use **text** for highlighting"
                                            )
                                        elif config.get("type") == "dropdown":
                                            current_value = current_text_values.get(field_name, config.get("default", ""))
                                            options = config.get("values", [])
                                            default_index = 0
                                            if current_value in options:
                                                default_index = options.index(current_value)
                                            text_input[field_name] = st.selectbox(
                                                f"{display_name}:",
                                                options=options,
                                                index=default_index
                                            )
                                    
                                    # Assets
                                    if "assets" in slide_config:
                                        for field_name, config in slide_config["assets"].items():
                                            if config.get("type") == "dropdown":
                                                options = config.get("values", [])
                                                default_value = config.get("default", options[0] if options else "")
                                                value = st.selectbox(
                                                    f"{field_name.replace('_', ' ').title()}:",
                                                    options=options,
                                                    index=options.index(default_value) if default_value in options else 0
                                                )
                                                assets_input[field_name] = {"file_type": "path", "content": value}
                                    
                                    submitted = st.form_submit_button("Update Text", type="primary")
                                    
                                    if submitted:
                                        try:
                                            from src.workflows.editors import text_editor
                                            
                                            # Process assets
                                            session_id_temp = str(uuid.uuid4())
                                            for key, value in assets_input.items():
                                                if value.get("file_type") == "path":
                                                    assets_input[key] = value.get("content")
                                            
                                            new_image_bytes = text_editor(
                                                template=slide_config,
                                                page_name=result_page_name,
                                                image_edits={},
                                                video_edits=slide_config.get("video_edits", {}),
                                                text=text_input,
                                                assets=assets_input,
                                                session_id=session_id_temp,
                                                is_video=False
                                            )
                                            
                                            if new_image_bytes:
                                                st.session_state[edit_key] = new_image_bytes
                                                st.success("✅ Text updated successfully!")
                                                st.rerun()
                                            else:
                                                st.error("Failed to update text")
                                                
                                        except Exception as e:
                                            st.error(f"Error updating text: {e}")

                            except Exception as e:
                                st.error(f"Text editing not available: {e}")
                        else:
                            st.info("Text editing not available for this slide type")
        else:
            st.warning("No images found for this slide")

    # Clear results button
    if st.button("🗑️ Clear Results", type="secondary"):
        # Clear session state
        keys_to_clear = [
            key for key in st.session_state.keys()
            if key.startswith(f"content_result_{session_id}") or key.startswith(f"edited_{session_id}")
        ]
        for key in keys_to_clear:
            del st.session_state[key]
        if "latest_session_id" in st.session_state:
            del st.session_state["latest_session_id"]
        if "latest_page_name" in st.session_state:
            del st.session_state["latest_page_name"]
        if "show_results" in st.session_state:
            del st.session_state["show_results"]
        st.rerun()


def show_media_results(session_id: str, result: dict, slides: list, selected_slide_idx: int):
    """Display media content results (with both without_text and with_text overlays)"""

    # Show selected slide details
    if selected_slide_idx is not None and selected_slide_idx < len(slides):
        selected_slide = slides[selected_slide_idx]

        # Show images with radio button selection
        slide_images = selected_slide.get("images", [])
        if slide_images:
            tab_names = [f"Image {i+1}" for i in range(len(slide_images))]
            tabs = st.tabs(tab_names)

            for tab_idx, (tab, img_data) in enumerate(zip(tabs, slide_images)):
                with tab:
                    # Show image type and model info
                    st.caption(
                        f"{img_data.get('type', 'unknown').title()} ({img_data.get('model', 'unknown')})"
                    )

                    # Show both versions side by side
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Without Text Overlay**")
                        try:
                            # Validate base64 data exists
                            base64_data = img_data.get("images", {}).get("without_text", {}).get("image_base64")
                            if not base64_data:
                                raise ValueError("No base64 image data found")
                            
                            without_text_data = base64.b64decode(base64_data)
                            if not without_text_data:
                                raise ValueError("Decoded image data is empty")
                            
                            st.image(without_text_data, width=400)
                            st.download_button(
                                label="⬇️ Download",
                                data=without_text_data,
                                file_name=f"slide_{selected_slide_idx+1}_post_{tab_idx+1}_without_text.png",
                                mime="image/png",
                                key=f"download_without_{session_id}_{selected_slide_idx}_{tab_idx}",
                            )
                        except Exception as e:
                            st.error(f"Failed to load image without text")

                    with col2:
                        st.markdown("**With Text Overlay**")

                        # Check if there's an edited version in session state
                        edit_key = (
                            f"edited_{session_id}_{selected_slide_idx}_{tab_idx}"
                        )

                        if edit_key in st.session_state:
                            # Show edited image
                            st.image(st.session_state[edit_key], width=400)
                            st.download_button(
                                label="⬇️ Download Edited",
                                data=st.session_state[edit_key],
                                file_name=f"slide_{selected_slide_idx+1}_post_{tab_idx+1}_edited.png",
                                mime="image/png",
                                key=f"download_edited_{session_id}_{selected_slide_idx}_{tab_idx}",
                            )

                            # Clear edit button
                            if st.button(
                                "🗑️ Clear Edit",
                                key=f"clear_{session_id}_{selected_slide_idx}_{tab_idx}",
                            ):
                                del st.session_state[edit_key]
                                st.rerun()
                        else:
                            # Show original with text
                            try:
                                # Validate base64 data exists
                                base64_data = img_data.get("images", {}).get("with_text", {}).get("image_base64")
                                if not base64_data:
                                    raise ValueError("No base64 image data found")
                                
                                with_text_data = base64.b64decode(base64_data)
                                if not with_text_data:
                                    raise ValueError("Decoded image data is empty")
                                
                                st.image(with_text_data, width=400)
                                st.download_button(
                                    label="⬇️ Download",
                                    data=with_text_data,
                                    file_name=f"slide_{selected_slide_idx+1}_post_{tab_idx+1}_with_text.png",
                                    mime="image/png",
                                    key=f"download_with_{session_id}_{selected_slide_idx}_{tab_idx}",
                                )
                            except Exception as e:
                                st.error(f"Failed to load image with text")

                        # Text editor section
                        st.markdown("---")
                        st.markdown("**Edit Text**")

                        # Get template and slide info for text editor
                        template_type = result.get("template_type", "timeline")
                        result_page_name = result.get("page_name", st.session_state.get("latest_page_name", "scoopwhoop"))
                        template = get_template_config(template_type, result_page_name)
                        slide_name = selected_slide.get("name", "headline_slide")
                        if (
                            "slides" in template
                            and slide_name in template["slides"]
                        ):
                            try:
                                current_text_values = selected_slide.get(
                                    "text_template", {}
                                )
                                
                                # Validate base64 data exists
                                base64_data = img_data.get("images", {}).get("without_text", {}).get("image_base64")
                                if not base64_data:
                                    raise ValueError("No base64 image data found for editing")
                                
                                without_text_bytes = base64.b64decode(base64_data)
                                if not without_text_bytes:
                                    raise ValueError("Decoded image data is empty for editing")
                                # Get original image without text for editing

                                # Get the specific slide configuration
                                slide_config = template["slides"][slide_name]
                                new_image, submitted = text_editor_form(
                                    text_values=current_text_values,
                                    content_bytes=without_text_bytes,
                                    template={"slides": {slide_name: slide_config}},
                                    slide_name=slide_name,
                                    form_key=f"edit_form_{session_id}_{selected_slide_idx}_{tab_idx}",
                                    page_name=result_page_name,
                                    show_image_upload=True,
                                    session_id=session_id
                                )

                                if submitted and new_image:
                                    st.session_state[edit_key] = new_image
                                    st.success("✅ Text edited successfully!")
                                    st.rerun()

                            except Exception as e:
                                st.error(f"No image to edit")
                                print(e)
                        else:
                            st.info(
                                "Text editing not available for this slide type"
                            )
        else:
            st.warning("No images found for this slide")

        # Clear results button
        if st.button("🗑️ Clear Results", type="secondary"):
            # Clear session state
            keys_to_clear = [
                key
                for key in st.session_state.keys()
                if key.startswith(f"content_result_{session_id}")
            ]
            for key in keys_to_clear:
                del st.session_state[key]
            if "latest_session_id" in st.session_state:
                del st.session_state["latest_session_id"]
            if "latest_page_name" in st.session_state:
                del st.session_state["latest_page_name"]
            if "show_results" in st.session_state:
                del st.session_state["show_results"]
                st.rerun()
