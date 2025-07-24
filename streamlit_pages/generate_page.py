import streamlit as st
import asyncio
import time
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

from src.workflow import workflow
from src.mongo_client import get_mongo_client
from src.utils import pil_image_to_bytes

def show_generate_page():
    st.title("🎨 Generate Social Media Posts")
    st.markdown("Upload a reference image to generate 3 unique social media posts")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a reference image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload an image that contains text or content you want to transform into social media posts"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Reference Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:

            def on_click():
                with col2:
                    generate_posts(pil_image_to_bytes(image), store_in_db)
            
            st.subheader("Generation Settings")
            store_in_db = True
            # Generate button
            st.button("🚀 Generate Posts", type="primary", use_container_width=True, on_click=on_click)

def generate_posts(image_bytes:bytes, store_in_db):
    """Generate posts with loading progress"""
    
    # Create progress tracking
    progress_container = st.empty()
    status_container = st.empty()
    
    with progress_container.container():
        st.markdown("### 🔄 Generating Posts...")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Step 1: Initialize
        progress_bar.progress(10)
        status_text.text("📋 Analyzing reference image...")
        time.sleep(1)  # Small delay for UI feedback
        
        # Step 2: Start workflow
        progress_bar.progress(30)
        status_text.text("🤖 Extracting content and generating descriptions...")
        
        # Run async workflow
        document_id = asyncio.run(workflow(image_bytes, store_in_db=store_in_db))
        
        # Step 3: Progress updates
        progress_bar.progress(60)
        status_text.text("🎨 Creating images...")
        time.sleep(1)
        
        progress_bar.progress(80)
        status_text.text("📱 Generating final posts...")
        time.sleep(1)
        
        # Step 4: Complete
        progress_bar.progress(100)
        status_text.text("✅ Posts generated successfully!")
        
        # Display results if available
        if store_in_db and document_id:
            show_generated_results(document_id)
            
    except Exception as e:
        progress_bar.progress(0)
        st.error(f"❌ Error generating posts: {str(e)}")
        status_text.text("Generation failed")
    
    finally:
        # Clear progress after 3 seconds
        time.sleep(3)
        progress_container.empty()
        status_container.empty()

def show_generated_results(document_id):
    """Display the generated results"""
    try:
        mongo_client = get_mongo_client()
        result = mongo_client.get_workflow_result(document_id)
        mongo_client.close()
        
        if result:
            st.markdown("### 📱 Generated Posts Preview")
            
            # Display images
            images = result.get("images", [])
            if images:
                st.markdown("#### Generated Images")
                
                for i, img_data in enumerate(images[:3]):  # Show first 3
                    with st.expander(f"Post {img_data['index']}", expanded=i==0):
                        col1, col2 = st.columns(2)
                        
                        # Show without text
                        with col1:
                            st.write("**Without Text Overlay**")
                            try:
                                without_text_b64 = img_data["images"]["without_text"]["image_base64"]
                                without_text_img = base64.b64decode(without_text_b64)
                                st.image(without_text_img, use_container_width=True)
                            except:
                                st.error("Failed to load image without text")
                        
                        # Show with text
                        with col2:
                            st.write("**With Text Overlay**")
                            try:
                                with_text_b64 = img_data["images"]["with_text"]["image_base64"]
                                with_text_img = base64.b64decode(with_text_b64)
                                st.image(with_text_img, use_container_width=True)
                            except:
                                st.error("Failed to load image with text")
                        
                        # st.write(f"**Description:** {img_data['description']}")
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}") 