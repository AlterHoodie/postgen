import uuid
import os
from pathlib import Path
import re
from datetime import datetime

from src.services.rapidapi import get_tweet_data
from src.workflows.editors import text_editor
from src.templates.twitter.tweet_image import tweet_image_template
from src.templates.twitter.tweet_text import tweet_text_template
from src.templates.twitter.tweet_tag import tweet_tag_template

from src.clients import download_image, download_video

def clean_tweet_text(tweet_text: str) -> str:
    """
    Clean tweet text by removing URLs and special characters
    """
    return re.sub(r'https://t\.co/\w+', '', tweet_text)

async def create_tweet_content_from_url(tweet_url: str, crop_type: str = "cover") -> tuple[bytes, bool]:
    """
    Complete workflow to create Twitter content from tweet URL
    
    Args:
        tweet_url: Twitter URL to extract data from
        
    Returns:
        tuple: (Generated image/video content bytes, is_video boolean)
    """
    # First fetch tweet data
    tweet_data = get_tweet_data(tweet_url)
    # Then create content from data
    tweet_data["crop_type"] = crop_type
    return await create_tweet_content(tweet_data)

async def handle_quoted_media(tweet_data: dict, session_id: str) -> tuple[dict, dict, bool]:
    """Handle quoted media and return assets, text updates, and video flag"""
    assets = {}
    text_updates = {}
    is_video = False
    
    if not tweet_data["quoted_media"]:
        return assets, text_updates, is_video
    
    media_type = tweet_data["quoted_media"][0]["type"]
    media_url = tweet_data["quoted_media"][0]["url"]

    profile_pic_data = await download_image(tweet_data["quoted_profile_picture_url"])
    profile_pic_path = f"./data/twitter/temp/quoted_profile_pic_{session_id}.png"
    with open(profile_pic_path, "wb") as f:
        f.write(profile_pic_data.getvalue())
    assets["quoted_profile_pic"] = profile_pic_path
    
    # Add quoted user info to text
    text_updates.update({
        "quoted_user_name": tweet_data["quoted_username"],
        "quoted_user_handle": f"@{tweet_data['quoted_userhandle']}",
        "quoted_date": tweet_data["quoted_created_at"],
        "quoted_tweet_text": clean_tweet_text(tweet_data["quoted_text"])
    })
    
    if media_type == "photo":
        media_data = await download_image(media_url)
        media_path = f"./data/twitter/temp/quoted_background_image_{session_id}.png"
        with open(media_path, "wb") as f:
            f.write(media_data.getvalue())
        assets["background_image"] = media_path
    elif media_type == "video" or media_type == "animated_gif":
        media_data = await download_video(media_url)
        media_path = f"./data/twitter/temp/quoted_background_video_{session_id}.mp4"
        with open(media_path, "wb") as f:
            f.write(media_data.getvalue())
        assets["background_video"] = media_path
        is_video = True
    
    return assets, text_updates, is_video

async def handle_main_media(tweet_data: dict, session_id: str) -> tuple[dict, dict, bool]:
    """Handle main tweet media and return assets, video edits, and video flag"""
    assets = {}
    video_edits = {}
    is_video = False
    
    if not tweet_data["media"]:
        return assets, video_edits, is_video
    
    media_type = tweet_data["media"][0]["type"]
    media_url = tweet_data["media"][0]["url"]
    
    if media_type == "photo":
        media_data = await download_image(media_url)
        media_path = f"./data/twitter/temp/background_image_{session_id}.png"
        with open(media_path, "wb") as f:
            f.write(media_data.getvalue())
        assets["background_image"] = media_path
    elif media_type == "video" or media_type == "animated_gif":
        media_data = await download_video(media_url)
        media_path = f"./data/twitter/temp/background_video_{session_id}.mp4"
        with open(media_path, "wb") as f:
            f.write(media_data.getvalue())
        assets["background_video"] = media_path
        is_video = True
        video_edits = {"crop_type": "cover", "type": "video_overlay", "class_name":"tweet-media", "padding":85}
    
    return assets, video_edits, is_video

async def create_tweet_content(tweet_data: dict) -> tuple[bytes, bool]:
    """
    Complete workflow to create Twitter content from tweet data
    
    Args:
        tweet_data: Twitter data dictionary with structure:
            {
                'username': str,
                'userhandle': str, 
                'is_verified': bool,
                'profile_picture_url': str,
                'text': str,
                'media': [{'type': str, 'url': str}, ...],
                'crop_type': ["cover", "contain"],
                'quoted_username': str,
                'quoted_userhandle': str,
                'quoted_is_verified': bool,
                'quoted_profile_picture_url': str,
                'quoted_text': str,
                'quoted_media': [{'type': str, 'url': str}, ...],
                'quoted_created_at': str
            }
        
    Returns:
        tuple: (Generated image/video content bytes, is_video boolean)
    """
    # Generate session ID for file management
    session_id = str(uuid.uuid4())[:8]

    # Create temp directory for twitter assets
    temp_dir = Path("./data/twitter/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # Download and save main user profile picture
    profile_pic_data = await download_image(tweet_data["profile_picture_url"])
    profile_pic_path = f"./data/twitter/temp/profile_pic_{session_id}.png"
    with open(profile_pic_path, "wb") as f:
        f.write(profile_pic_data.getvalue())
    
    # Set up assets dictionary
    assets = {
        "profile_pic": profile_pic_path
    }
    # Set up text dictionary
    text = {
        "user_name": tweet_data["username"],
        "user_handle": f"@{tweet_data['userhandle']}",
        "tweet_text": clean_tweet_text(tweet_data["text"]),
        "add_verified_badge": tweet_data["is_verified"]
    }
    image_edits = {"crop_type": tweet_data["crop_type"]}
    video_edits = {}
    
    # Handle quoted media
    quoted_assets, quoted_text, quoted_is_video = await handle_quoted_media(tweet_data, session_id)
    assets.update(quoted_assets)
    text.update(quoted_text)
    
    # Handle main media
    main_assets, main_video_edits, main_is_video = await handle_main_media(tweet_data, session_id)
    assets.update(main_assets)
    
    # Set video edits for quoted media if needed
    if quoted_is_video:
        video_edits = {"crop_type": "cover", "type": "video_overlay", "class_name":"quoted-video", "padding":105}
    elif main_is_video:
        video_edits = main_video_edits
    
    is_video = quoted_is_video or main_is_video
    
    # Choose template based on media presence
    if tweet_data["quoted_media"]:
        template = tweet_tag_template["slides"]["twitter_quote_post"]
    elif tweet_data["media"]:
        template = tweet_image_template["slides"]["twitter_post"]
    else:
        template = tweet_text_template["slides"]["text_based_slide"]
    
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
    tweet_url = "https://x.com/divyanshiwho/status/1962363623675707434"
    result, is_video = asyncio.run(create_tweet_content_from_url(tweet_url))
    with open("./data_/tweet_test.png", "wb") as f:
        f.write(result)