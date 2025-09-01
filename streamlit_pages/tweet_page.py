import streamlit as st
import asyncio
import time
import concurrent.futures
import re
from pathlib import Path

from src.workflows.tweet_creator import create_tweet_content
from src.services.rapidapi import get_tweet_data


def show_tweet_page():
    """Main tweet page interface with two-step workflow"""
    st.title("🐦 Tweet Content Generator")

    # Initialize session state
    if "tweet_data" not in st.session_state:
        st.session_state["tweet_data"] = None
    if "show_tweet_form" not in st.session_state:
        st.session_state["show_tweet_form"] = False

    # Create two-column layout: form on left, preview on right
    col_left, col_right = st.columns([1, 1])

    with col_left:
        # Step 1: URL Input and Fetch Tweet Data
        if not st.session_state["show_tweet_form"]:
            show_url_input_step()
        else:
            # Step 2: Show editable form with tweet data
            show_tweet_form_step()

    with col_right:
        st.markdown("### Preview")
        
        # Show results if available
        if st.session_state.get("show_tweet_results") and st.session_state.get("latest_tweet_result"):
            show_tweet_preview()
        else:
            # Placeholder content when no results
            show_preview_placeholder()


def show_url_input_step():
    """Step 1: URL input and tweet data fetching"""
    st.markdown("### Step 1: Enter Tweet URL")
    
    # URL input
    tweet_url = st.text_input(
        "Enter Twitter/X URL",
        placeholder="https://x.com/username/status/1234567890",
        help="Paste the full URL of the tweet you want to convert"
    )

    # Validate URL format
    if tweet_url and not is_valid_tweet_url(tweet_url):
        st.error("❌ Please enter a valid Twitter/X URL")
        return

    if tweet_url:
        # Fetch tweet data button
        if st.button(
            "📥 Fetch Tweet Data", type="primary", use_container_width=True
        ):
            fetch_tweet_data(tweet_url)

    # Reset button if tweet data exists
    if st.session_state.get("tweet_data"):
        if st.button("🔄 Enter New URL", use_container_width=True):
            reset_tweet_workflow()


def show_tweet_form_step():
    """Step 2: Show editable form with tweet data"""
    st.markdown("### Step 2: Edit Tweet Data")
    
    tweet_data = st.session_state["tweet_data"]
    
    if not tweet_data:
        st.error("No tweet data found. Please fetch tweet data first.")
        return

    # Create editable form
    with st.form("tweet_edit_form"):
        st.markdown("#### User Information")
        
        username = st.text_input("Username", value=tweet_data.get("username", ""))
        userhandle = st.text_input("Handle (without @)", value=tweet_data.get("userhandle", ""))
        is_verified = st.checkbox("Verified Account", value=tweet_data.get("is_verified", False))

        st.markdown("#### Tweet Content")
        tweet_text = st.text_area(
            "Tweet Text", 
            value=tweet_data.get("text", ""),
            height=100,
            help="Edit the tweet text as needed"
        )

        # Media information (read-only for now)
        st.markdown("#### Media")
        if tweet_data.get("media"):
                media = tweet_data["media"][0]
                st.info(f"📁 Media: {media.get('type', 'Unknown')} - {media.get('url', 'No URL')}")
        else:
            st.info("📝 No media attached to this tweet")

        # Generate button
        submitted = st.form_submit_button(
            "🎨 Generate Tweet Content", 
            type="primary", 
            use_container_width=True
        )

        if submitted:
            # Update tweet data with edited values
            updated_tweet_data = {
                "username": username,
                "userhandle": userhandle,
                "is_verified": is_verified,
                "profile_picture_url": tweet_data.get("profile_picture_url", ""),
                "text": tweet_text,
                "media": tweet_data.get("media", [])
            }
            generate_tweet_content_from_data(updated_tweet_data)

    # Back button
    if st.button("⬅️ Back to URL Input"):
        reset_tweet_workflow()


def fetch_tweet_data(tweet_url: str):
    """Fetch tweet data from URL"""
    progress_container = st.empty()
    
    with progress_container.container():
        st.markdown("### 📥 Fetching Tweet Data...")
        progress_bar = st.progress(0)
        status_text = st.empty()

    try:
        # Step 1: Validate URL
        progress_bar.progress(25)
        status_text.text("🔍 Validating URL...")
        time.sleep(0.5)

        # Step 2: Fetch data
        progress_bar.progress(50)
        status_text.text("📡 Fetching tweet data from API...")
        
        tweet_data = get_tweet_data(tweet_url)
        
        # Step 3: Process data
        progress_bar.progress(75)
        status_text.text("⚙️ Processing tweet data...")
        time.sleep(0.5)

        # Step 4: Complete
        progress_bar.progress(100)
        status_text.text("✅ Tweet data fetched successfully!")

        # Store in session state
        st.session_state["tweet_data"] = tweet_data
        st.session_state["original_tweet_url"] = tweet_url
        st.session_state["show_tweet_form"] = True

        time.sleep(1)
        st.rerun()

    except Exception as e:
        progress_bar.progress(0)
        st.error(f"❌ Error fetching tweet data: {str(e)}")
        status_text.text("Fetch failed")

    finally:
        time.sleep(2)
        progress_container.empty()


def generate_tweet_content_from_data(tweet_data: dict):
    """Generate tweet content from tweet data"""
    progress_container = st.empty()

    with progress_container.container():
        st.markdown("### 🎨 Generating Tweet Content...")
        progress_bar = st.progress(0)
        status_text = st.empty()

    try:
        # Step 1: Initialize
        progress_bar.progress(20)
        status_text.text("📋 Preparing content generation...")
        time.sleep(1)

        # Step 2: Download assets
        progress_bar.progress(40)
        status_text.text("📷 Downloading media assets...")
        
        # Step 3: Generate content
        progress_bar.progress(60)
        status_text.text("🎨 Creating styled content...")

        # Run async workflow with tweet data
        def run_tweet_workflow():
            return asyncio.run(create_tweet_content(tweet_data))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_tweet_workflow)
            result_bytes, is_video = future.result()

        # Step 4: Finalize
        progress_bar.progress(80)
        status_text.text("📱 Finalizing content...")
        time.sleep(1)

        # Step 5: Complete
        progress_bar.progress(100)
        status_text.text("✅ Tweet content generated successfully!")

        # Store result in session state
        st.session_state["latest_tweet_result"] = result_bytes
        st.session_state["is_video"] = is_video
        st.session_state["latest_tweet_data"] = tweet_data
        st.session_state["show_tweet_results"] = True

        time.sleep(1)
        st.rerun()

    except Exception as e:
        progress_bar.progress(0)
        st.error(f"❌ Error generating tweet content: {str(e)}")
        status_text.text("Generation failed")

    finally:
        # Clear progress after 2 seconds
        time.sleep(2)
        progress_container.empty()


def reset_tweet_workflow():
    """Reset the workflow to start over"""
    st.session_state["tweet_data"] = None
    st.session_state["show_tweet_form"] = False
    st.session_state["show_tweet_results"] = False
    st.session_state["latest_tweet_result"] = None
    st.rerun()


def show_preview_placeholder():
    """Show placeholder content when no results are available"""
    st.markdown(
        """
        <div style="
            border: 2px dashed #ccc; 
            border-radius: 10px; 
            padding: 40px; 
            text-align: center; 
            color: #666;
            min-height: 300px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
        ">
            <h3>📱 Generated Content Preview</h3>
            <p>Your styled tweet content will appear here</p>
            <p style="font-size: 0.8em;">Fetch tweet data and generate to see the magic!</p>
        </div>
        """, 
        unsafe_allow_html=True
    )


def show_tweet_preview():
    """Display the generated tweet content in the preview column"""
    try:
        result_bytes = st.session_state.get("latest_tweet_result")
        is_video = st.session_state.get("is_video")
        if not result_bytes:
            st.error("No results found")
            return

        # Display the generated content
        if is_video:
            st.video(result_bytes, width=500)
        else:
            st.image(result_bytes, width=500)
        
        # Download button
        st.download_button(
            label="⬇️ Download",
            data=result_bytes,
            file_name=f"tweet_content_{int(time.time())}.{is_video and 'mp4' or 'png'}",
            mime=is_video and "video/mp4" or "image/png",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"Error displaying preview: {str(e)}")


def is_valid_tweet_url(url: str) -> bool:
    """Validate if the URL is a valid Twitter/X URL"""
    twitter_patterns = [
        r'https?://(www\.)?twitter\.com/\w+/status/\d+',
        r'https?://(www\.)?x\.com/\w+/status/\d+',
    ]
    
    return any(re.match(pattern, url) for pattern in twitter_patterns)


# Legacy function for compatibility
def show_tweet_results():
    """Display the generated tweet content results (legacy function for compatibility)"""
    show_tweet_preview()


if __name__ == "__main__":
    show_tweet_page()