import uuid
import os
from pathlib import Path
import re

from src.services.rapidapi import get_tweet_data
from src.workflows.editors import text_editor
from src.templates.twitter.tweet_image import tweet_image_template
from src.templates.twitter.tweet_text import tweet_text_template

from src.clients import download_image, download_video

def clean_tweet_text(tweet_text: str) -> str:
    """
    Clean tweet text by removing URLs and special characters
    """
    return re.sub(r'https://t\.co/\w+', '', tweet_text)

async def create_tweet_content(tweet_url: str) -> bytes:
    """
    Complete workflow to create Twitter content from tweet URL
    
    Args:
        tweet_url: Twitter URL to extract data from
        
    Returns:
        bytes: Generated image/video content
    """
    # Generate session ID for file management
    session_id = str(uuid.uuid4())[:8]
    
    # Get tweet data
    tweet_data = get_tweet_data(tweet_url)
    # Create temp directory for twitter assets
    temp_dir = Path("./data/twitter/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Download and save profile picture
    profile_pic_data = await download_image(tweet_data["profile_picture_url"])
    profile_pic_path = f"./data/twitter/temp/profile_pic_{session_id}.png"
    with open(profile_pic_path, "wb") as f:
        f.write(profile_pic_data.getvalue())
    
    # Set up assets dictionary
    assets = {
        "profile_pic": profile_pic_path
    }
    
    # Handle media if present
    media_data = None
    is_video = False
    
    if tweet_data["media"]:
        media_type = tweet_data["media"][0]["type"]
        if media_type == "photo":
            media_url = tweet_data["media"][0]["url"]
            media_data = await download_image(media_url)
            media_path = f"./data/twitter/temp/background_image_{session_id}.png"
            with open(media_path, "wb") as f:
                f.write(media_data.getvalue())
            assets["background_image"] = media_path
        elif media_type == "video" or media_type == "animated_gif":
            media_url = tweet_data["media"][0]["url"]  # Fixed: removed video_details
            media_data = await download_video(media_url)
            media_path = f"./data/twitter/temp/background_video_{session_id}.mp4"
            with open(media_path, "wb") as f:
                f.write(media_data.getvalue())
            assets["background_video"] = media_path
            is_video = True
    
    # Set up text dictionary
    text = {
        "user_name": tweet_data["username"],
        "user_handle": f"@{tweet_data['userhandle']}",
        "tweet_text": clean_tweet_text(tweet_data["text"]),
        "add_verified_badge": tweet_data["is_verified"]
    }
    
    # Choose template based on media presence
    if tweet_data["media"]:
        template = tweet_image_template["slides"]["twitter_post"]
    else:
        template = tweet_text_template["slides"]["text_based_slide"]
    
    # Set up edit parameters
    image_edits = {"crop_type": "cover"}
    video_edits = {"crop_type": "cover", "type": "video_overlay", "class_name":"tweet-media", "padding":85}
    
    # Call text_editor to generate content
    result = text_editor(
        template=template,
        page_name="twitter",
        image_edits=image_edits,
        video_edits=video_edits,
        text=text,
        assets=assets,
        session_id=session_id,
        is_video=is_video
    )
    
    return result, is_video


if __name__ == "__main__":
    import asyncio
    tweet_url = "https://x.com/Riocasm/status/1957472065084440822"
    result = asyncio.run(create_tweet_content(tweet_url))
    with open("./data_/tweet_test.png", "wb") as f:
        f.write(result)