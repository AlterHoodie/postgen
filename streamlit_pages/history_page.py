import streamlit as st
import time
from datetime import datetime
import base64
import logging
import pytz

from src.mongo_client import get_mongo_client
from src.utils import extract_text_from_html, regenerate_image_from_html, update_html_content

def show_history_page():
    st.title("📜 Generation History")
    st.markdown("View previously generated social media posts")
    
    # Loading overlay while fetching data
    if 'history_loaded' not in st.session_state:
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
        st.markdown("""
        <div class="loading-overlay">
            <div>
                <div class="spinner"></div>
                <div>Loading history...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
    history_data = st.session_state.get('history_data', [])
    
    if not history_data:
        st.info("📭 No generation history found. Generate some posts first!")
        return
    
    st.success(f"📊 Found {len(history_data)} previous generations")
    
    # Display each workflow result
    for i, workflow_result in enumerate(history_data):
        with st.expander(
            f"🎨 Generation {i+1} - {workflow_result.get('session_id', 'Unknown')} "
            f"({format_date(workflow_result.get('created_at'))})",
            expanded=(i == 0)
        ):
            display_workflow_result(workflow_result)

def display_workflow_result(workflow_result):
    """Display a single workflow result"""
    # Basic info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"**Session ID:** {workflow_result.get('session_id', 'N/A')}")
    with col2:
        st.write(f"**Date:** {format_date(workflow_result.get('created_at'))}")
    with col3:
        st.write(f"**Total Images:** {workflow_result.get('total_images', 0)}")
    
    # Images
    images = workflow_result.get('images', [])
    if images:
        st.markdown("#### 🖼️ Generated Images")
        
        # Create tabs for each image
        if len(images) > 1:
            tab_names = [f"Post {i+1}" for i in range(len(images))]
            tabs = st.tabs(tab_names)
            
            for idx, (tab, img_data) in enumerate(zip(tabs, images)):
                with tab:
                    display_image_pair(img_data, workflow_result_index=workflow_result.get('session_id', 'unknown'), image_index=idx)
        else:
            # Single image
            display_image_pair(images[0], workflow_result_index=workflow_result.get('session_id', 'unknown'), image_index=0)

def display_image_pair(img_data, workflow_result_index=0, image_index=0):
    """Display a pair of images (with and without text)"""
    col1, col2 = st.columns(2)
    
    # Create unique keys for this specific image
    session_id = workflow_result_index
    unique_key = f"{session_id}_{image_index}"
    
    # Without text
    if img_data.get('type', ''):
        st.write(f"**Type**: **{img_data.get('type', '').capitalize()} Image**")
    with col1:
        st.write("**Without Text Overlay**")
        try:
            without_text_b64 = img_data["images"]["without_text"]["image_base64"]
            without_text_img = base64.b64decode(without_text_b64)
            st.image(without_text_img, width=450)
            
            # Download button
            st.download_button(
                label="⬇️ Download",
                data=without_text_img,
                file_name=img_data["images"]["without_text"]["filename"],
                mime="image/png",
                key=f"download_without_{unique_key}"
            )
        except Exception as e:
            logging.error(f"Failed to load image without text: {e}")
            st.error("Failed to load image without text")
    
    # With text
    with col2:
        st.write("**With Text Overlay**")
        
        # Create unique key for this image's edited version
        edited_key = f"edited_image_{unique_key}"
        
        # Check if we have an edited version in session state
        if edited_key in st.session_state:
            # Show the edited image
            st.image(st.session_state[edited_key], width=450)
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
                st.image(with_text_img, width=450)
                
                # Download button
                st.download_button(
                    label="⬇️ Download",
                    data=with_text_img,
                    file_name=img_data["images"]["with_text"]["filename"],
                    mime="image/png",
                    key=f"download_with_{unique_key}"
                )
            except Exception as e:
                st.error("Failed to load image with text")
        
        # Add Edit button
        if st.button("✏️ Edit Text", key=f"edit_btn_{unique_key}"):
            st.session_state[f"show_edit_{unique_key}"] = True
        
        # Show edit form if button was clicked
        if st.session_state.get(f"show_edit_{unique_key}", False):
            show_edit_form(img_data, unique_key)

def show_edit_form(img_data, unique_key):
    """Show the edit form for modifying text"""
    try:
        html_content = img_data.get("html", "")
        if not html_content:
            st.error("No HTML content available for editing")
            return
        
        # Extract current text
        current_headline, current_sub_text = extract_text_from_html(html_content)
        
        st.markdown("---")
        st.markdown("**✏️ Edit Text Content**")
        
        # Create edit form
        with st.form(key=f"edit_form_{unique_key}"):
            # Text inputs with current values
            new_headline = st.text_area(
                "Headline (HTML):", 
                value=current_headline,
                height=100,
                help="You can use HTML tags like <span class='yellow'> to highlight text"
            )
            
            new_sub_text = st.text_area(
                "Sub Text (HTML):", 
                value=current_sub_text,
                height=80,
                help="You can use <br/> tags for line breaks"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                regenerate_clicked = st.form_submit_button("🔄 Regenerate Image", type="primary")
            with col2:
                cancel_clicked = st.form_submit_button("❌ Cancel")
            
            if regenerate_clicked:
                with st.spinner("Regenerating image..."):
                    # Update HTML with new content
                    updated_html = update_html_content(html_content, new_headline, new_sub_text)
                    
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
            
            if cancel_clicked:
                # Hide the edit form
                st.session_state[f"show_edit_{unique_key}"] = False
                st.rerun()
                
    except Exception as e:
        st.error(f"Error in edit form: {e}")


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
