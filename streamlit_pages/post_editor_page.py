import streamlit as st
import base64
from PIL import Image
from io import BytesIO

from src.workflows.edit_image import image_workflow
from src.workflows.edit_video import video_workflow

def show_post_editor_page():
    st.title("🎨 Post Editor")
    st.markdown("Create video and image posts with custom text overlays")
    
    # Tab selection for image or video
    tab1, tab2 = st.tabs(["📷 Image Post", "🎥 Video Post"])
    
    with tab1:
        create_image_post()
    
    with tab2:
        create_video_post()

def create_image_post():
    st.markdown("### Create Image Post")
    st.markdown("Upload an image and add headline/subtext to create a post")
    
    # File uploader for image
    col1, col2 = st.columns([1, 2])
    with col1:
        uploaded_image = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image to use as background",
            key="image_uploader"
        )
    
    if uploaded_image is not None:
        
        with col1:
            # Show highlighting info
            
            # Text inputs
            headline = st.text_area(
                "Headline:",
                placeholder="Enter your headline here...",
                help="Use **text** to highlight words in yellow",
                height=100,
                key="image_headline",
                value=""
            )
            
            subtext = st.text_area(
                "Subtext:",
                placeholder="Enter your subtext here...",
                height=80,
                key="image_subtext",
                value=""
            )
            
            new_source = st.text_input("Source:", value="", key="image_source")
            is_trigger = st.checkbox("Trigger Warning", value=False, key="image_trigger")
            
            # Generate button
            if st.button("🚀 Generate Image Post", type="primary", use_container_width=True, key="generate_image"):
                if subtext.strip() or headline.strip() or new_source.strip():
                    generate_image_post(uploaded_image, headline=headline, subtext=subtext, source=new_source, is_trigger=is_trigger)
                else:
                    st.error("Please enter a field")
            
            # Clear button (only show if generated image exists)
            if 'generated_image' in st.session_state:
                if st.button("🔄 Create New Post", key="clear_image"):
                    del st.session_state['generated_image']
                    st.rerun()
            st.info("💡 **Simple Highlighting:** Use `**text**` to make text yellow.")
        
        with col2:
            sub_col1, sub_col2 = st.columns([1, 1])
            with sub_col1:
                st.subheader("Original Image")
                image = Image.open(uploaded_image)
                st.image(image, caption="Uploaded Image", width=400)
            
            # Show generated image below original if it exists
            if 'generated_image' in st.session_state:
                with sub_col2:
                    st.subheader("Generated Post")
                    st.image(st.session_state['generated_image'], width=400)
                
                    # Download button
                    st.download_button(
                        label="⬇️ Download Image Post",
                        data=st.session_state['generated_image'],
                        file_name="image_post.png",
                        mime="image/png"
                    )

def create_video_post():
    st.markdown("### Create Video Post")
    st.markdown("Upload a video and add headline/subtext to create a post")
    
    # File uploader for video
    uploaded_video = st.file_uploader(
        "Choose a video",
        type=['mp4', 'mov', 'avi'],
        help="Upload a video to use as background",
        key="video_uploader"
    )
    
    if uploaded_video is not None:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Show highlighting info
            st.info("💡 **Simple Highlighting:** Use `**text**` to make text yellow.")
            
            # Text inputs
            headline = st.text_area(
                "Headline:",
                placeholder="Enter your headline here...",
                help="Use **text** to highlight words in yellow",
                height=100,
                key="video_headline",
                value=""
            )
            
            subtext = st.text_area(
                "Subtext:",
                placeholder="Enter your subtext here...",
                height=80,
                key="video_subtext",
                value=""
            )

            new_source = st.text_input("Source:", value="", key="video_source")
            is_trigger = st.checkbox("Trigger Warning", value=False, key="video_trigger")
            
            # Generate button
            if st.button("🚀 Generate Video Post", type="primary", use_container_width=True, key="generate_video"):
                if subtext.strip() or headline.strip() or new_source.strip() or is_trigger:
                    generate_video_post(uploaded_video, subtext=subtext, headline=headline, source=new_source, is_trigger=is_trigger)
                else:
                    st.error("Please enter a field")
            
            # Clear button (only show if generated video exists)
            if 'generated_video' in st.session_state:
                if st.button("🔄 Create New Post", key="clear_video"):
                    del st.session_state['generated_video']
                    st.rerun()
        
        with col2:
            sub_col1, sub_col2 = st.columns([1, 1])
            with sub_col1:
                st.subheader("Original Video")
                st.video(uploaded_video, width=300)
            
            # Show generated video below original if it exists
            if 'generated_video' in st.session_state:
                with sub_col2:
                    st.subheader("Generated Post")
                    st.video(st.session_state['generated_video'], width=400)
                
                    # Download button
                    st.download_button(
                    label="⬇️ Download Video Post",
                    data=st.session_state['generated_video'],
                    file_name="video_post.mp4",
                    mime="video/mp4"
                    )

def generate_image_post(uploaded_image, headline, subtext, source, is_trigger):
    """Generate image post with text overlay"""
    
    # Create progress tracking
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown("### 🔄 Generating Image Post...")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Step 1: Prepare image
        progress_bar.progress(20)
        status_text.text("📷 Preparing image...")
        
        # Convert PIL image to bytes
        image_bytes = BytesIO()
        image = Image.open(uploaded_image)
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        
        # Step 2: Generate overlay
        progress_bar.progress(60)
        status_text.text("🎨 Creating text overlay...")
        
        # Call the image workflow
        result_bytes = image_workflow(image_bytes, subtext, headline, source, is_trigger)
        
        if result_bytes:
            # Step 3: Complete
            progress_bar.progress(100)
            status_text.text("✅ Image post generated successfully!")
            
            # Display result in the right column
            # Find the existing columns and update the right column
            st.session_state['generated_image'] = result_bytes
        else:
            st.error("❌ Failed to generate image post")
            
    except Exception as e:
        st.error(f"❌ Error generating image post: {str(e)}")
    
    finally:
        # Clear progress after 2 seconds
        import time
        time.sleep(2)
        progress_container.empty()

def generate_video_post(uploaded_video, headline, subtext, source, is_trigger):
    """Generate video post with text overlay"""
    
    # Create progress tracking
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown("### 🔄 Generating Video Post...")
        progress_bar = st.progress(0)
        status_text = st.empty()
    
    try:
        # Step 1: Prepare video
        progress_bar.progress(10)
        status_text.text("🎥 Preparing video...")
        
        # Get video bytes
        video_bytes = uploaded_video.read()
        
        # Step 2: Generate overlay
        progress_bar.progress(30)
        status_text.text("🎨 Creating text overlay...")
        
        # Step 3: Process video
        progress_bar.progress(50)
        status_text.text("🔄 Processing video (this may take a few minutes)...")
        
        # Call the video workflow
        result_bytes = video_workflow(video_bytes, subtext, headline, source, is_trigger)
        
        if result_bytes:
            # Step 4: Complete
            progress_bar.progress(100)
            status_text.text("✅ Video post generated successfully!")
            
            # Display result in the right column
            st.session_state['generated_video'] = result_bytes
        else:
            st.error("❌ Failed to generate video post")
            
    except Exception as e:
        st.error(f"❌ Error generating video post: {str(e)}")
    
    finally:
        # Clear progress after 2 seconds
        import time
        time.sleep(2)
        progress_container.empty()