import streamlit as st
import time
import base64
import uuid
import logging
import pytz

from src.services.mongo_client import get_mongo_client
from src.templates import get_template_config
from streamlit_pages.page_editor import text_editor_form


def show_history_page():
    st.title("📜 Content Generation History")
    st.markdown("View previously generated content slides and workflows")

    # Loading overlay while fetching data
    if "history_loaded" not in st.session_state:
        st.session_state.history_loaded = False

    # Show loading overlay on first load or refresh
    if not st.session_state.history_loaded:
        load_history_data()
    else:
        # Show refresh button
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            if st.button("🔄 Refresh", type="secondary"):
                st.session_state.history_loaded = False
                st.rerun()

        display_history()


def show_loading_overlay():
    """Show loading overlay while fetching history data"""
    loading_container = st.empty()

    with loading_container.container():
        st.markdown(
            """
        <div class="loading-overlay">
            <div>
                <div class="spinner"></div>
                <div>Loading history...</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Simulate loading time
        progress = st.progress(0)
        for i in range(100):
            progress.progress(i + 1)
            time.sleep(0.01)  # Small delay for visual effect

    # Clear loading overlay
    loading_container.empty()


def load_history_data():
    """Load history data from database"""
    try:
        mongo_client = get_mongo_client()
        history_data = mongo_client.get_recent_workflows(limit=15)
        mongo_client.close()

        st.session_state.history_data = history_data
        st.session_state.history_loaded = True

        st.rerun()
    except Exception as e:
        st.error(f"❌ Error loading history: {str(e)}")
        st.session_state.history_data = []
        st.session_state.history_loaded = True


def display_history():
    """Display the loaded history data"""
    history_data = st.session_state.get("history_data", [])

    if not history_data:
        st.info("📭 No generation history found. Generate some content first!")
        return

    # Filter for content creator workflows
    content_workflows = [
        w for w in history_data if w.get("workflow_type") == "content_creator"
    ]

    if not content_workflows:
        st.info("📭 No content workflows found. Generate some content first!")
        return

    st.success(f"📊 Found {len(content_workflows)} content generations")

    # Display each workflow result
    for i, workflow_result in enumerate(content_workflows):
        headline = workflow_result.get("headline", "Unknown")
        template_type = workflow_result.get("template_type", "Unknown")
        total_slides = workflow_result.get("total_slides", 0)

        with st.expander(
            f"🎬 {headline[:500]} - {template_type.title()} ({total_slides} slides) - "
            f"{format_date(workflow_result.get('created_at'))}",
            expanded=(i == 0),
        ):
            display_content_workflow(workflow_result)


def display_content_workflow(workflow_result):
    """Display a content creator workflow result with similar layout to generate page"""
    # Basic info
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(f"**Template:** {workflow_result.get('template_type', 'N/A').title()}")
    with col2:
        st.write(f"**Total Slides:** {workflow_result.get('total_slides', 0)}")
    with col3:
        st.write(f"**Session ID:** {workflow_result.get('session_id', 'N/A')}")

    # Check for errors
    if workflow_result.get("error"):
        st.error(f"❌ **Error:** {workflow_result['error']}")
        return

    # Get slides data
    slides = workflow_result.get("slides", [])
    if not slides:
        st.warning("No slides found in this workflow")
        return

    # Check if this is text-only content
    is_text_only = slides[0].get("image_description", "") == ""
    session_id = workflow_result.get("session_id", "unknown")
    
    if is_text_only:
        show_history_text_only_results(workflow_result, slides, session_id)
    else:
        show_history_media_results(workflow_result, slides, session_id)


def show_history_text_only_results(workflow_result, slides, session_id):
    """Display text-only content history results"""
    # Slide selection dropdown
    slide_options = [
        f"Slide {i+1}: {slide.get('name', f'slide_{i}')}"
        for i, slide in enumerate(slides)
    ]

    selected_slide_idx = st.selectbox(
        "Select a slide:",
        range(len(slide_options)),
        format_func=lambda i: slide_options[i],
        key=f"history_slide_select_{session_id}",
    )

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
                        edit_key = f"history_edited_{session_id}_{selected_slide_idx}_{tab_idx}"

                        if edit_key in st.session_state:
                            # Show edited image
                            st.image(st.session_state[edit_key], width=400)
                            st.download_button(
                                label="⬇️ Download Edited",
                                data=st.session_state[edit_key],
                                file_name=f"history_{session_id}_slide_{selected_slide_idx+1}_post_{tab_idx+1}_edited.png",
                                mime="image/png",
                                key=f"history_download_edited_{session_id}_{selected_slide_idx}_{tab_idx}",
                            )

                            # Clear edit button
                            if st.button(
                                "🗑️ Clear Edit",
                                key=f"history_clear_{session_id}_{selected_slide_idx}_{tab_idx}",
                            ):
                                del st.session_state[edit_key]
                                st.rerun()
                        else:
                            # Show original with text
                            try:
                                with_text_data = base64.b64decode(
                                    img_data["images"]["with_text"]["image_base64"]
                                )
                                st.image(with_text_data, width=400)
                                st.download_button(
                                    label="⬇️ Download",
                                    data=with_text_data,
                                    file_name=f"history_{session_id}_slide_{selected_slide_idx+1}_post_{tab_idx+1}.png",
                                    mime="image/png",
                                    key=f"history_download_with_{session_id}_{selected_slide_idx}_{tab_idx}",
                                )
                            except Exception as e:
                                st.error(f"Failed to load image: {e}")

                    with col2:
                        # Text editor section
                        st.markdown("**Edit Text**")

                        # Get template and slide info for text editor
                        template_type = workflow_result.get("template_type", "writeup")
                        page_name = workflow_result.get("page_name", "the_sarcastic_indian")
                        template = get_template_config(template_type, page_name)
                        slide_name = selected_slide.get("name", "headline_slide")
                        
                        if "slides" in template and slide_name in template["slides"]:
                            try:
                                current_text_values = selected_slide.get("text_template", {})
                                
                                # Get the specific slide configuration
                                slide_config = template["slides"][slide_name]
                                
                                # Use text-only editor for editing
                                with st.form(key=f"history_text_edit_form_{session_id}_{selected_slide_idx}_{tab_idx}"):
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
                                                page_name=page_name,
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


def show_history_media_results(workflow_result, slides, session_id):
    """Display media content history results"""
    # Slide selection dropdown
    slide_options = [
        f"Slide {i+1}: {slide.get('name', f'slide_{i}')}"
        for i, slide in enumerate(slides)
    ]

    selected_slide_idx = st.selectbox(
        "Select a slide:",
        range(len(slide_options)),
        format_func=lambda i: slide_options[i],
        key=f"history_slide_select_{session_id}",
    )

    # Show selected slide details
    if selected_slide_idx is not None and selected_slide_idx < len(slides):
        selected_slide = slides[selected_slide_idx]

        # Show images with tabs selection
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
                        st.markdown("**Without Text**")
                        try:
                            without_text_data = base64.b64decode(
                                img_data["images"]["without_text"]["image_base64"]
                            )
                            st.image(without_text_data, width=400)
                            st.download_button(
                                label="⬇️ Download",
                                data=without_text_data,
                                file_name=f"history_{session_id}_slide_{selected_slide_idx+1}_post_{tab_idx+1}_without_text.png",
                                mime="image/png",
                                key=f"history_download_without_{session_id}_{selected_slide_idx}_{tab_idx}",
                            )
                        except Exception as e:
                            st.error(f"Failed to load image without text: {e}")

                    with col2:
                        st.markdown("**With Text Overlay**")

                        # Check if there's an edited version in session state
                        edit_key = f"history_edited_{session_id}_{selected_slide_idx}_{tab_idx}"

                        if edit_key in st.session_state:
                            # Show edited image
                            st.image(st.session_state[edit_key], width=400)
                            st.download_button(
                                label="⬇️ Download Edited",
                                data=st.session_state[edit_key],
                                file_name=f"history_{session_id}_slide_{selected_slide_idx+1}_post_{tab_idx+1}_edited.png",
                                mime="image/png",
                                key=f"history_download_edited_{session_id}_{selected_slide_idx}_{tab_idx}",
                            )

                            # Clear edit button
                            if st.button(
                                "🗑️ Clear Edit",
                                key=f"history_clear_{session_id}_{selected_slide_idx}_{tab_idx}",
                            ):
                                del st.session_state[edit_key]
                                st.rerun()
                        else:
                            # Show original with text
                            try:
                                with_text_data = base64.b64decode(
                                    img_data["images"]["with_text"]["image_base64"]
                                )
                                st.image(with_text_data, width=400)
                                st.download_button(
                                    label="⬇️ Download",
                                    data=with_text_data,
                                    file_name=f"history_{session_id}_slide_{selected_slide_idx+1}_post_{tab_idx+1}_with_text.png",
                                    mime="image/png",
                                    key=f"history_download_with_{session_id}_{selected_slide_idx}_{tab_idx}",
                                )
                            except Exception as e:
                                st.error(f"Failed to load image with text: {e}")

                        # Text editor section
                        st.markdown("---")
                        st.markdown("**Edit Text**")

                        # Get template and slide info for text editor
                        template_type = workflow_result.get("template_type", "timeline")
                        template = get_template_config(template_type, page_name = workflow_result.get("page_name", "scoopwhoop"))
                        slide_name = selected_slide.get("name", "headline_slide")

                        if "slides" in template and slide_name in template["slides"]:
                            # Get original image without text for editing
                            try:
                                without_text_bytes = base64.b64decode(
                                    img_data["images"]["without_text"]["image_base64"]
                                )

                                # Extract current text values from slide data
                                current_text_values = selected_slide.get(
                                    "text_template", {}
                                )

                                new_image = text_editor_form(
                                    text_values=current_text_values,
                                    content_bytes=without_text_bytes,
                                    template=template,
                                    slide_name=slide_name,
                                    form_key=f"history_edit_form_{session_id}_{selected_slide_idx}_{tab_idx}",
                                    show_image_upload=True,
                                    page_name = workflow_result.get("page_name", "scoopwhoop"),
                                )

                                if new_image[0]:  # new_image is a tuple (bytes, bool)
                                    st.session_state[edit_key] = new_image[0]
                                    st.success("✅ Text edited successfully!")
                                    st.rerun()

                            except Exception as e:
                                st.error(f"Text editor error: {e}")
                        else:
                            st.info("Text editing not available for this slide type")
        else:
            st.warning("No images found for this slide")


def format_date(date_obj):
    """Format UTC datetime object to IST and return a readable string"""
    if date_obj:
        if isinstance(date_obj, str):
            return date_obj
        try:
            # Convert UTC to IST
            utc = pytz.utc
            ist = pytz.timezone("Asia/Kolkata")

            if date_obj.tzinfo is None:
                # Assume it's naive UTC (from MongoDB)
                date_obj = utc.localize(date_obj)

            ist_date = date_obj.astimezone(ist)
            return ist_date.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            return str(date_obj)
    return "Unknown"
