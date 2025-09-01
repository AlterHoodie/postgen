import logging

import streamlit as st

from streamlit_pages.generate_page import show_generate_page
from streamlit_pages.page_editor import show_post_editor_page
from streamlit_pages.tweet_page import show_tweet_page
from streamlit_pages.history_page import show_history_page
from streamlit_pages.sources_page import show_sources_page
from src.workflows.sources import start_background_daemon

# Configure page
st.set_page_config(
    page_title="Scoopwhoop Post Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Custom CSS for loading states
st.markdown(
    """
<style>
/* Loading overlay styles */
.loading-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;
    color: white;
    font-size: 1.5em;
}

/* Simple spinner */
.spinner {
    border: 4px solid #f3f3f3;
    border-top: 4px solid #FF6B35;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin: 0 auto 20px;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Hide default streamlit menu */
.css-14xtw13.e8zbici0 { display: none !important; }

/* Style the sidebar */
.css-1d391kg { background-color: #f8f9fa; }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def start_daemon_on_server_startup():
    """Start the background daemon when server starts - runs only once."""
    daemon = start_background_daemon()
    logger.info("Background sources daemon started! 🚀")
    return daemon

def main():
    # ⚡ Start daemon when server starts (runs only once)
    start_daemon_on_server_startup()
    
    # Sidebar navigation
    st.sidebar.title("🎨 Post Generator")
    st.sidebar.markdown("---")

    # Navigation
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Generate Posts", "Sources", "Post Editor", "Tweet Generator", "History"],
        key="page_selector",
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("Generate social media posts from reference images using AI.")

    # Route to appropriate page
    if page == "Generate Posts":
        show_generate_page()
    if page == "Post Editor":
        show_post_editor_page()
    elif page == "Tweet Generator":
        show_tweet_page()
    elif page == "History":
        show_history_page()
    elif page == "Sources":
        show_sources_page()


if __name__ == "__main__":
    main()
