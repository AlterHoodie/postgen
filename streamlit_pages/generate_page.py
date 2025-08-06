import streamlit as st
import asyncio
import time
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image

from workflows.generate_posts import generate_posts_workflow
from src.mongo_client import get_mongo_client
from src.utils import pil_image_to_bytes, extract_text_from_html, regenerate_image_from_html, update_html_content, convert_simple_text_to_html
import concurrent.futures

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
    
    # Always show the latest generated results if they exist
            show_latest_results()

def generate_posts(image_bytes: bytes, store_in_db):
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
        
        # Run async workflow in a separate thread with its own event loop
        def run_workflow():
            return asyncio.run(generate_posts_workflow(image_bytes, store_in_db=store_in_db))
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_workflow)
            document_id = future.result()  # This will block until completion
        
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
            # Store the latest document_id in session state
            st.session_state['latest_document_id'] = document_id
            
    except Exception as e:
        progress_bar.progress(0)
        st.error(f"❌ Error generating posts: {str(e)}")
        status_text.text("Generation failed")
    
    finally:
        # Clear progress after 3 seconds
        time.sleep(3)
        progress_container.empty()
        status_container.empty()

def show_generated_results(document_id, show_title=True):
    """Display the generated results"""
    try:
        # Check if we already have the result in session state
        result_key = f"generated_result_{document_id}"
        
        if result_key not in st.session_state:
            # Fetch from database and store in session state
            mongo_client = get_mongo_client()
            result = mongo_client.get_workflow_result(document_id)
            mongo_client.close()
            st.session_state[result_key] = result
        else:
            # Use cached result from session state
            result = st.session_state[result_key]
        
        if result:
            if show_title:
                st.markdown("### 📱 Generated Posts Preview")
            
            # Display images
            images = result.get("images", [])
            if images:
                st.markdown("#### Images")
                
                for i, img_data in enumerate(images):  # Show first 3
                    with st.expander(f"Post {i+1}", expanded=i==0):
                        col1, col2 = st.columns(2)
                        
                        # Show without text
                        st.write(f"**Type**: **{img_data.get('type', '').capitalize()} Image**")
                        with col1:
                            st.write("**Without Text Overlay**")
                            try:
                                without_text_b64 = img_data["images"]["without_text"]["image_base64"]
                                without_text_img = base64.b64decode(without_text_b64)
                                st.image(without_text_img, use_container_width=True)
                                st.download_button(
                                    label="⬇️ Download",
                                    data=without_text_img,
                                    file_name=img_data["images"]["without_text"]["filename"],
                                    mime="image/png",
                                    key=img_data["images"]["without_text"]["filename"]
                                )
                            except:
                                st.error("Failed to load image without text")
                        
                        # Show with text
                        with col2:
                            st.write("**With Text Overlay**")
                            
                            # Create unique key for this image
                            unique_key = f"{document_id}_{i}"
                            edited_key = f"edited_image_{unique_key}"
                            
                            # Check if we have an edited version in session state
                            if edited_key in st.session_state:
                                # Show the edited image
                                st.image(st.session_state[edited_key], use_container_width=True)
                                st.download_button(
                                    label="⬇️ Download Edited",
                                    data=st.session_state[edited_key],
                                    file_name=f"edited_{img_data['images']['with_text']['filename']}",
                                    mime="image/png",
                                    key=f"download_edited_{unique_key}"
                                )
                            else:
                                # Show the original image
                                try:
                                    with_text_b64 = img_data["images"]["with_text"]["image_base64"]
                                    with_text_img = base64.b64decode(with_text_b64)
                                    st.image(with_text_img, use_container_width=True)
                                    st.download_button(
                                        label="⬇️ Download",
                                        data=with_text_img,
                                        file_name=img_data["images"]["with_text"]["filename"],
                                        mime="image/png",
                                        key=f"download_original_{unique_key}"
                                    )
                                except:
                                    st.error("Failed to load image with text")
                            
                            # Add Edit button
                            if st.button("✏️ Edit Text", key=f"edit_btn_{unique_key}"):
                                st.session_state[f"show_edit_{unique_key}"] = True
                            
                            # Show edit form if button was clicked
                            if st.session_state.get(f"show_edit_{unique_key}", False):
                                show_edit_form_generate(img_data, unique_key)
                        
                        # st.write(f"**Description:** {img_data['description']}")
    except Exception as e:
        st.error(f"Error displaying results: {str(e)}")

def show_edit_form_generate(img_data, unique_key):
    """Show the edit form for modifying text in generate page"""
    try:
        html_content = img_data.get("html", "")
        if not html_content:
            st.error("No HTML content available for editing")
            return
        
        # Extract current text (with \highlight syntax)
        current_headline, current_sub_text = extract_text_from_html(html_content)
        
        # Show simple syntax info
        st.info("💡 **Simple Highlighting:** Use `**text**` to make text yellow.")
        
        # Create edit form
        with st.form(key=f"edit_form_{unique_key}"):
            # Text inputs with current values
            new_headline = st.text_area(
                "Headline:", 
                value=current_headline,
                height=100,
                help="Type your headline. Use **text** around words you want highlighted in yellow. Use multiple lines for line breaks."
            )
            
            new_sub_text = st.text_area(
                "Sub Text:", 
                value=current_sub_text,
                height=80,
                help="Type your sub-text. Use multiple lines for line breaks."
            )
            
            col1, col3 = st.columns(2)
            with col1:
                regenerate_clicked = st.form_submit_button("🔄 Regenerate Image", type="primary")

            with col3:
                # Only show clear button if there's an edited version
                edited_key = f"edited_image_{unique_key}"
                clear_clicked = False
                if edited_key in st.session_state:
                    clear_clicked = st.form_submit_button("🔄 Show Original", type="secondary")
            
            if regenerate_clicked:
                with st.spinner("Regenerating image..."):
                    # Convert simple text to styled HTML
                    new_headline_html, new_sub_text_html = convert_simple_text_to_html(new_headline, new_sub_text)
                    
                    # Update HTML with new content
                    updated_html = update_html_content(html_content, new_headline_html, new_sub_text_html)
                    
                    # Regenerate image (pass original image data for background image extraction)
                    new_image_bytes = regenerate_image_from_html(
                        updated_html, 
                        unique_key.split('_')[0], 
                        unique_key.split('_')[1], 
                        original_image_data=img_data
                    )
                    
                    if new_image_bytes:
                        # Store the edited image in session state
                        st.session_state[f"edited_image_{unique_key}"] = new_image_bytes
                        st.success("✅ Image regenerated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to regenerate image")
            
            if clear_clicked:
                # Clear the edited image and show original
                edited_key = f"edited_image_{unique_key}"
                if edited_key in st.session_state:
                    del st.session_state[edited_key]
                # Hide the edit form
                st.session_state[f"show_edit_{unique_key}"] = False
                st.success("✅ Cleared edit - showing original image")
                st.rerun()
                
    except Exception as e:
        st.error(f"Error in edit form: {e}")

def show_latest_results():
    """Always show the latest generated results if they exist"""
    latest_document_id = st.session_state.get('latest_document_id')
    
    if latest_document_id:
        st.markdown("---")  # Visual separator
        
        # Add a header with clear button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 📱 Latest Generated Posts")
        with col2:
            if st.button("🗑️ Clear Results", type="secondary", help="Clear the latest results from view"):
                # Clear all related session state
                keys_to_clear = [key for key in st.session_state.keys() 
                               if key.startswith(f'generated_result_{latest_document_id}') 
                               or key.startswith(f'edited_image_{latest_document_id}')
                               or key.startswith(f'show_edit_{latest_document_id}')]
                for key in keys_to_clear:
                    del st.session_state[key]
                del st.session_state['latest_document_id']
                st.rerun()
        
        show_generated_results(latest_document_id, show_title=False) 