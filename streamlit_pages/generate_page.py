import streamlit as st
import asyncio
import time
import base64

from src.workflows.content_creator import workflow
from src.services.mongo_client import get_mongo_client
import concurrent.futures
from src.templates.timeline import timeline_template
from src.templates.thumbnail import thumbnail_template
from src.templates.writeup import writeup_template

def get_template_config(template_type: str) -> dict:
    """Get template configuration based on type"""
    if template_type == "timeline":
        return timeline_template
    elif template_type == "thumbnail":
        return thumbnail_template
    elif template_type == "writeup":
        return writeup_template
    else:
        raise ValueError(f"Unknown template type: {template_type}")

def show_generate_page():
    st.title("🎨 Generate Content Slides")
    st.markdown("Enter a headline to generate content slides with images")
    
    # Input for headline
    headline = st.text_input(
        "Enter Headline",
        placeholder="e.g., UttarKashi Cloud Burst India",
        help="Enter the headline for your content"
    )
    
    # Template selection
    template_options = {
        "Timeline": "timeline",
        "Thumbnail": "thumbnail", 
        "Writeup": "writeup"
    }
    
    selected_template = st.selectbox(
        "Select Template",
        options=list(template_options.keys()),
        help="Choose the template style for your content"
    )
    
    if headline:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Generate button
            if st.button("🚀 Generate Content", type="primary", use_container_width=True):
                generate_content(headline, template_options[selected_template])
        
        with col2:
            # Show latest results link
            if st.session_state.get('latest_session_id'):
                if st.button("📱 Show Latest Results", use_container_width=True):
                    st.session_state['show_results'] = True
    
    # Show results if available
    if st.session_state.get('show_results') and st.session_state.get('latest_session_id'):
        show_content_results(st.session_state['latest_session_id'])

def generate_content(headline: str, template_type: str):
    """Generate content slides with loading progress"""
    
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
            return asyncio.run(workflow(headline=headline, template=template, save=True))
        
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
        
        # Store session_id in session state
        st.session_state['latest_session_id'] = session_id
        st.session_state['show_results'] = True
        
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
        
        # Get slides data
        slides = result.get("slides", [])
        if not slides:
            st.warning("No slides found in results")
            return
        
        # Two column layout: original image (left) and slides (right)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 Original Reference")
            # Show headline and template info
            st.info(f"**Headline:** {result.get('headline', 'N/A')}")
            st.info(f"**Template:** {result.get('template_type', 'N/A').title()}")
            
            # Show first slide's first image as reference (if available)
            if slides and slides[0].get('images'):
                first_image = slides[0]['images'][0]
                try:
                    img_data = base64.b64decode(first_image['image_base64'])
                    st.image(img_data, caption="Reference Image", use_container_width=True)
                except:
                    st.error("Failed to load reference image")
        
        with col2:
            st.subheader("🎬 Generated Slides")
            
            # Slide selection dropdown
            slide_options = [f"Slide {i+1}: {slide.get('name', f'slide_{i}')}" for i, slide in enumerate(slides)]
            selected_slide_idx = st.selectbox(
                "Select a slide:",
                range(len(slide_options)),
                format_func=lambda i: slide_options[i]
            )
            
            # Show selected slide details
            if selected_slide_idx is not None and selected_slide_idx < len(slides):
                selected_slide = slides[selected_slide_idx]
                
                # Display slide info
                st.write(f"**Name:** {selected_slide.get('name', 'N/A')}")
                st.write(f"**Description:** {selected_slide.get('image_description', 'N/A')}")
                
                # Show images with radio button selection
                slide_images = selected_slide.get('images', [])
                if slide_images:
                    st.markdown("#### Select an image:")
                    
                    # Radio button for image selection
                    image_options = [f"{img.get('type', 'unknown').title()} ({img.get('model', 'unknown')})" for img in slide_images]
                    
                    if len(image_options) > 1:
                        selected_img_idx = st.radio(
                            "Choose image:",
                            range(len(image_options)),
                            format_func=lambda i: image_options[i],
                            key=f"img_select_{session_id}_{selected_slide_idx}"
                        )
                    else:
                        selected_img_idx = 0
                    
                    # Display selected image
                    if selected_img_idx is not None and selected_img_idx < len(slide_images):
                        selected_image = slide_images[selected_img_idx]
                        
                        try:
                            img_data = base64.b64decode(selected_image['image_base64'])
                            st.image(img_data, use_container_width=True)
                            
                            # Download button
                            st.download_button(
                                label="⬇️ Download Image",
                                data=img_data,
                                file_name=f"slide_{selected_slide_idx+1}_{selected_image.get('type', 'image')}.png",
                                mime="image/png",
                                key=f"download_{session_id}_{selected_slide_idx}_{selected_img_idx}"
                            )
                        except Exception as e:
                            st.error(f"Failed to load image: {e}")
                else:
                    st.warning("No images found for this slide")
                    
        # Clear results button
        if st.button("🗑️ Clear Results", type="secondary"):
            # Clear session state
            keys_to_clear = [key for key in st.session_state.keys() if key.startswith(f'content_result_{session_id}')]
            for key in keys_to_clear:
                del st.session_state[key]
            if 'latest_session_id' in st.session_state:
                del st.session_state['latest_session_id']
            if 'show_results' in st.session_state:
                del st.session_state['show_results']
                st.rerun()
                
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")