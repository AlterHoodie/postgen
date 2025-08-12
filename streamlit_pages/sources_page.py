from datetime import datetime
import base64
import asyncio
import concurrent.futures
import time

import streamlit as st
import pandas as pd
import pytz

from src.workflows.sources import get_sources_summary
from src.services.mongo_client import get_mongo_client
from src.templates import get_template_config
from src.workflows.content_creator import workflow
from streamlit_pages.page_editor import text_editor_form


def show_sources_page():
    """Display sources management page with original images and generation form."""
    st.title("📊 Instagram Sources")
    
    summary = get_sources_summary(limit=10)
    
    if summary["error"]:
        st.error(f"Error: {summary['error']}")
        return
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Sources", summary["total_sources"])
    
    with col2:
        if summary["latest_timestamp"]:
            latest_dt = datetime.fromtimestamp(summary["latest_timestamp"],tz=pytz.timezone("Asia/Kolkata"))
            st.metric("Latest Post", latest_dt.strftime("%Y-%m-%d %H:%M"))
        else:
            st.metric("Latest Post", "None")
    
    with col3:
        st.metric("Recent Posts", len(summary["latest_posts"]))
    
    # Display recent posts with image and generation form
    if summary["latest_posts"]:
        st.subheader("🔥 Recent Posts - Generate Content")
        
        for idx, post in enumerate(summary["latest_posts"]):
            # Create a container for each post
            with st.container():
                st.markdown("---")
                
                # Create two columns: left for original image, right for generation
                col_image, col_generate = st.columns([1, 2])
                
                with col_image:
                    st.markdown(f"**Post {idx + 1}**")
                    
                    # Display post metadata
                    st.caption(f"📅 {datetime.fromtimestamp(post.get('taken_at', 0)).strftime('%Y-%m-%d %H:%M')}")
                    st.caption(f"❤️ {post.get('like_count', 0)} likes | 💬 {post.get('comment_count', 0)} comments")
                    
                    # Display original Instagram media (first item only)
                    media = post.get("media_bytes", "")
                    if media:
                        image_bytes = base64.b64decode(media.get("image_bytes"))
                        media_type = media.get("type")
                        
                        if image_bytes:
                            if media_type == "image" or media_type == "thumbnail":
                                st.image(image_bytes, width=400)
                            elif media_type == "video":
                                st.video(image_bytes)
                        else:
                            st.warning("No media available")
                    else:
                        # Show post info without media
                        st.info("No media available for this post")
                    
                    # Show caption preview
                    caption = post.get("caption", "")
                    if caption:
                        if len(caption) > 200:
                            caption_preview = caption[:200] + "..."
                        else:
                            caption_preview = caption
                        st.text_area("Caption:", value=caption_preview, height=100, disabled=True, key=f"caption_{idx}")
                
                with col_generate:
                    st.markdown(f"**Generate Content from Post {idx + 1}**")
                    
                    # Generation form
                    with st.form(key=f"generate_form_{idx}"):
                        # Use caption as default headline or let user modify
                        default_headline = post.get("caption", "") if post.get("caption") else ""
                        
                        headline = st.text_area(
                            "Headline for Content Generation",
                            value=default_headline,
                            placeholder="Enter headline for content generation",
                            key=f"headline_{idx}"
                        )
                        
                        # Template selection
                        template_options = {
                            "Timeline": "timeline",
                            "Thumbnail": "thumbnail", 
                            "Writeup": "writeup",
                        }
                        
                        selected_template = st.selectbox(
                            "Select Template",
                            options=list(template_options.keys()),
                            help="Choose the template style for your content",
                            key=f"template_{idx}"
                        )
                        
                        # Generate button
                        submitted = st.form_submit_button(
                            "🚀 Generate Content",
                            type="primary",
                            use_container_width=True
                        )
                        
                        if submitted and headline:
                            # Store the post info and generate
                            session_key = f"generation_{idx}_{post.get('code', '')}"
                            generate_content_from_source(
                                headline,
                                template_options[selected_template],
                                session_key,
                                post
                            )
                    
                    # Show generation results if available
                    session_key = f"generation_{idx}_{post.get('code', '')}"
                    if st.session_state.get(f"{session_key}_completed"):
                        show_generation_results(session_key, f"results_{idx}")
    else:
        st.info("No posts found in sources collection")


def generate_content_from_source(headline: str, template_type: str, session_key: str, post_data: dict):
    """Generate content from a source post with progress tracking"""
    
    # Create progress tracking
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown("### 🔄 Generating Content...")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Get template configuration
        template = get_template_config(template_type)
        
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
        
        # Store session_id and post data in session state
        st.session_state[f"{session_key}_session_id"] = session_id
        st.session_state[f"{session_key}_completed"] = True
        st.session_state[f"{session_key}_post_data"] = post_data
        
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


def show_generation_results(session_key: str, container_key: str):
    """Display the generated content results for a specific source post"""
    try:
        session_id = st.session_state.get(f"{session_key}_session_id")
        if not session_id:
            st.error("No session ID found")
            return
        
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
        
        st.markdown("### 📱 Generated Results")
        
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
            key=f"{container_key}_slide_select"
        )
        
        # Show selected slide details
        if selected_slide_idx is not None and selected_slide_idx < len(slides):
            selected_slide = slides[selected_slide_idx]
            
            # Show images with tabs
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
                                base64_data = img_data.get("images", {}).get("without_text", {}).get("image_base64")
                                if base64_data:
                                    without_text_data = base64.b64decode(base64_data)
                                    st.image(without_text_data, width=300)
                                    st.download_button(
                                        label="⬇️ Download",
                                        data=without_text_data,
                                        file_name=f"slide_{selected_slide_idx+1}_img_{tab_idx+1}_without_text.png",
                                        mime="image/png",
                                        key=f"download_without_{container_key}_{selected_slide_idx}_{tab_idx}",
                                    )
                                else:
                                    st.error("No image data available")
                            except Exception as e:
                                st.error("Failed to load image without text")
                        
                        with col2:
                            st.markdown("**With Text Overlay**")
                            
                            # Check if there's an edited version in session state
                            edit_key = f"edited_{session_id}_{selected_slide_idx}_{tab_idx}"
                            
                            if edit_key in st.session_state:
                                # Show edited image
                                st.image(st.session_state[edit_key], width=300)
                                st.download_button(
                                    label="⬇️ Download Edited",
                                    data=st.session_state[edit_key],
                                    file_name=f"slide_{selected_slide_idx+1}_img_{tab_idx+1}_edited.png",
                                    mime="image/png",
                                    key=f"download_edited_{container_key}_{selected_slide_idx}_{tab_idx}",
                                )
                                
                                # Clear edit button
                                if st.button(
                                    "🗑️ Clear Edit",
                                    key=f"clear_{container_key}_{selected_slide_idx}_{tab_idx}",
                                ):
                                    del st.session_state[edit_key]
                                    st.rerun()
                            else:
                                # Show original with text
                                try:
                                    base64_data = img_data.get("images", {}).get("with_text", {}).get("image_base64")
                                    if base64_data:
                                        with_text_data = base64.b64decode(base64_data)
                                        st.image(with_text_data, width=300)
                                        st.download_button(
                                            label="⬇️ Download",
                                            data=with_text_data,
                                            file_name=f"slide_{selected_slide_idx+1}_img_{tab_idx+1}_with_text.png",
                                            mime="image/png",
                                            key=f"download_with_{container_key}_{selected_slide_idx}_{tab_idx}",
                                        )
                                    else:
                                        st.error("No image data available")
                                except Exception as e:
                                    st.error("Failed to load image with text")
                            
                            # Text editor section
                            st.markdown("---")
                            st.markdown("**Edit Text**")
                            
                            # Get template and slide info for text editor
                            template_type = result.get("template_type", "timeline")
                            template = get_template_config(template_type)
                            slide_name = selected_slide.get("name", "headline_slide")
                            
                            if (
                                "slides" in template
                                and slide_name in template["slides"]
                            ):
                                try:
                                    current_text_values = selected_slide.get("text_template", {})
                                    
                                    base64_data = img_data.get("images", {}).get("without_text", {}).get("image_base64")
                                    if base64_data:
                                        without_text_bytes = base64.b64decode(base64_data)
                                        
                                        new_image, submitted = text_editor_form(
                                            text_values=current_text_values,
                                            content_bytes=without_text_bytes,
                                            template=template,
                                            slide_name=slide_name,
                                            form_key=f"edit_form_{container_key}_{selected_slide_idx}_{tab_idx}",
                                            show_image_upload=True
                                        )
                                        
                                        if submitted and new_image:
                                            st.session_state[edit_key] = new_image
                                            st.success("✅ Text edited successfully!")
                                            st.rerun()
                                    else:
                                        st.error("No image data available for editing")
                                        
                                except Exception as e:
                                    st.error("Failed to load text editor")
                            else:
                                st.info("Text editing not available for this slide type")
            else:
                st.warning("No images found for this slide")
        
        # Clear results button
        if st.button("🗑️ Clear Results", type="secondary", key=f"clear_results_{container_key}"):
            # Clear session state for this generation
            keys_to_clear = [
                key for key in st.session_state.keys()
                if key.startswith(session_key) or key.startswith(f"content_result_{session_id}")
            ]
            for key in keys_to_clear:
                del st.session_state[key]
            st.rerun()
            
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")
