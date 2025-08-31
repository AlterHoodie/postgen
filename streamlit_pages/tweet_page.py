import streamlit as st
import asyncio
import time
import concurrent.futures
import re
from pathlib import Path

from src.workflows.tweet_creator import create_tweet_content


def show_tweet_page():
    """Main tweet page interface"""
    st.title("🐦 Tweet Content Generator")

    # Create two-column layout: form on left, picture on right
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### Enter Tweet Details")
        
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
            # Generate button
            if st.button(
                "🚀 Generate Tweet Content", type="primary", use_container_width=True
            ):
                generate_tweet_content(tweet_url)

    with col_right:
        st.markdown("### Preview")
        
        # Show results if available
        if st.session_state.get("show_tweet_results") and st.session_state.get("latest_tweet_result"):
            show_tweet_preview()
        else:
            # Placeholder content when no results
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
                    <p style="font-size: 0.8em;">Enter a tweet URL and click generate to see the magic!</p>
                </div>
                """, 
                unsafe_allow_html=True
            )


def is_valid_tweet_url(url: str) -> bool:
    """Validate if the URL is a valid Twitter/X URL"""
    twitter_patterns = [
        r'https?://(www\.)?twitter\.com/\w+/status/\d+',
        r'https?://(www\.)?x\.com/\w+/status/\d+',
    ]
    
    return any(re.match(pattern, url) for pattern in twitter_patterns)


def generate_tweet_content(tweet_url: str):
    """Generate tweet content with loading progress"""
    
    # Create progress tracking
    progress_container = st.empty()

    with progress_container.container():
        st.markdown("### 🔄 Generating Tweet Content...")
        progress_bar = st.progress(0)
        status_text = st.empty()

    try:
        # Step 1: Initialize
        progress_bar.progress(20)
        status_text.text("📋 Extracting tweet data...")
        time.sleep(1)

        # Step 2: Download assets
        progress_bar.progress(40)
        status_text.text("📷 Downloading media assets...")
        
        # Step 3: Generate content
        progress_bar.progress(60)
        status_text.text("🎨 Creating styled content...")

        # Run async workflow
        def run_tweet_workflow():
            return asyncio.run(create_tweet_content(tweet_url))

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
        st.session_state["latest_tweet_url"] = tweet_url
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


def show_tweet_preview():
    """Display the generated tweet content in the left column preview"""
    try:
        result_bytes = st.session_state.get("latest_tweet_result")
        is_video = st.session_state.get("is_video")
        if not result_bytes:
            st.error("No results found")
            return

        # Display the generated image
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


def show_tweet_results():
    """Display the generated tweet content results (legacy function for compatibility)"""
    # This function is kept for compatibility but redirects to the preview
    show_tweet_preview()


if __name__ == "__main__":
    show_tweet_page()
