import streamlit as st
import time
from datetime import datetime
import base64
import logging

from src.mongo_client import get_mongo_client

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
        history_data = mongo_client.get_recent_workflows(limit=20)
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
            tab_names = [f"Post {img['index']}" for img in images]
            tabs = st.tabs(tab_names)
            
            for tab, img_data in zip(tabs, images):
                with tab:
                    display_image_pair(img_data)
        else:
            # Single image
            display_image_pair(images[0])

def display_image_pair(img_data):
    """Display a pair of images (with and without text)"""
    st.write(f"**Description:** {img_data.get('description', 'N/A')}")
    
    col1, col2 = st.columns(2)
    
    # Without text
    with col1:
        st.write("**Without Text Overlay**")
        try:
            without_text_b64 = img_data["images"]["without_text"]["image_base64"]
            without_text_img = base64.b64decode(without_text_b64)
            st.image(without_text_img, width=300)
            
            # Download button
            st.download_button(
                label="⬇️ Download",
                data=without_text_img,
                file_name=img_data["images"]["without_text"]["filename"],
                mime="image/png",
                key=img_data["images"]["without_text"]["filename"]
            )
        except Exception as e:
            logging.error(f"Failed to load image without text: {e}")
            st.error("Failed to load image without text")
    
    # With text
    with col2:
        st.write("**With Text Overlay**")
        try:
            with_text_b64 = img_data["images"]["with_text"]["image_base64"]
            with_text_img = base64.b64decode(with_text_b64)
            st.image(with_text_img, width=300)
            
            # Download button
            st.download_button(
                label="⬇️ Download",
                data=with_text_img,
                file_name=img_data["images"]["with_text"]["filename"],
                mime="image/png",
                key=img_data["images"]["with_text"]["filename"]
            )
        except Exception as e:
            st.error("Failed to load image with text")

def format_date(date_obj):
    """Format datetime object to readable string"""
    if date_obj:
        if isinstance(date_obj, str):
            return date_obj
        try:
            return date_obj.strftime("%Y-%m-%d %H:%M")
        except:
            return str(date_obj)
    return "Unknown" 