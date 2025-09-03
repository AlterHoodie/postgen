import requests
import os 
from dotenv import load_dotenv
from typing import List
from datetime import datetime

from src.clients import sync_download_image

load_dotenv(override=True)
api_key = os.getenv("RAPID_API_KEY")

def call_rapid_api(url: str, params: dict, headers: dict) -> dict:
    tries = 3
    while tries > 0:
        print(f"API call, {tries} tries left")
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 404:
            raise Exception(f"Page Not Found: {response.status_code}")
        else:
            print(f"status_code:{response.status_code}:{response.content}")
            tries -= 1
            continue
    if tries == 0:
        raise Exception(f"Failed 3 Attempts : {response.json()}")


def extract_instagram_post_data(posts_data: List[dict]) -> List[dict]:
    """
    Extracts specific information from a list of Instagram post data dictionaries.

    Args:
        posts_data: A list of dictionaries, where each dictionary represents
                    an Instagram post's data (like the provided example).

    Returns:
        A list of dictionaries, where each dictionary contains the
        extracted information for a single post. Returns an empty list
        if the input is empty or invalid.
    """
    extracted_posts = []
    if not isinstance(posts_data, list):
        print("Error: Input must be a list of post dictionaries.")
        return []

    for post in posts_data:
        if not isinstance(post, dict):
            print(f"Warning: Skipping invalid item in list: {post}")
            continue

        post_info = {}
        post_info["code"] = post.get("code", "")
        post_info["taken_at"] = int(datetime.strptime(post.get("taken_at", "2025-08-29T05:38:02Z"), "%Y-%m-%dT%H:%M:%SZ").timestamp())
        
        # Add user information
        user_data = post.get("user", {})
        post_info["username"] = user_data.get("username", "")
        post_info["user_full_name"] = user_data.get("full_name", "")
        post_info["user_is_verified"] = user_data.get("is_verified", False)
        
        # Location information
        location_data = post.get("location", {})
        post_info["location_name"] = location_data.get("name", "") if location_data else ""
        
        # 1. Type of post
        media_type = post.get("media_type")
        if media_type == 1:
            post_info["type"] = "image"
        elif media_type == 2:
            post_info["type"] = "video"
        elif media_type == 8:
            post_info["type"] = "carousel"
        else:
            # Fallback or handle other types if necessary
            post_info["type"] = post.get("product_type", "unknown")

        # 2. Likes count
        post_info["like_count"] = post.get("like_count", 0)
        post_info["share_count"] = post.get("share_count", 0)

        # 3. Comments count
        post_info["comment_count"] = post.get("comment_count", 0)
        post_info["sponsor_tags"] = post.get("sponsor_tags", [])

        # 4. View/Play count (for videos)
        if post_info["type"] == "video" or post_info["type"] == "carousel":
            # Use play_count if available, fallback to view_count
            play_count = post.get("play_count")
            if play_count is None:
                play_count = post.get("view_count")  # Check alternative key

            post_info["played_count"] = play_count if play_count is not None else 0
        else:
            post_info["played_count"] = None  # Not applicable for images

        # 5. Extract hashtags and mentions from caption text
        caption_text = post.get("caption_text", "")
        hashtags = []
        mentions = []
        
        if caption_text:
            # Extract hashtags (words starting with #)
            import re
            hashtags = re.findall(r'#\w+', caption_text)
            # Extract mentions (words starting with @)
            mentions = re.findall(r'@\w+', caption_text)
        
        post_info["hashtags"] = hashtags
        post_info["mentions"] = mentions

        # 6. Is paid partnership
        post_info["is_paid_partnership"] = post.get("is_paid_partnership", False)

        # 7. Caption
        post_info["caption"] = caption_text

        # 8. Media list (URLs and types)
        media_list = []
        if post_info["type"] == "carousel":
            # New format uses 'resources' for carousel items
            carousel_items = post.get("resources", [])
            for item in carousel_items:
                # Check if it's an image or video within the carousel
                if item.get("media_type") == 1:  # Image
                    image_versions = item.get("image_versions", [])
                    if image_versions:
                        # Take the highest quality image (first in list)
                        media_list.append({
                            "url": image_versions[0].get("url"),
                            "type": "image"
                        })
                elif item.get("media_type") == 2:  # Video
                    # Check for direct video_url first
                    video_url = item.get("video_url")
                    if video_url:
                        media_list.append({
                            "url": video_url,
                            "type": "video"
                        })
                    else:
                        # Fallback to video_versions
                        video_versions = item.get("video_versions", [])
                        if video_versions:
                            media_list.append({
                                "url": video_versions[0].get("url"),
                                "type": "video"
                            })
                    
                    # Add thumbnail for video
                    thumbnail_url = item.get("thumbnail_url")
                    if thumbnail_url:
                        media_list.append({
                            "url": thumbnail_url,
                            "type": "thumbnail"
                        })

        elif post_info["type"] == "image":
            # For single images, use main image_versions
            image_versions = post.get("image_versions", [])
            if image_versions:
                # Take the highest quality image (first in list)
                media_list.append({
                    "url": image_versions[0].get("url"),
                    "type": "image"
                })

        elif post_info["type"] == "video":
            # Check for direct video_url first
            video_url = post.get("video_url")
            if video_url:
                media_list.append({
                    "url": video_url,
                    "type": "video"
                })
            else:
                # Fallback to video_versions
                video_versions = post.get("video_versions", [])
                if video_versions:
                    media_list.append({
                        "url": video_versions[0].get("url"),
                        "type": "video"
                    })
            
            # Add thumbnail for video
            thumbnail_url = post.get("thumbnail_url")
            if thumbnail_url:
                media_list.append({
                    "url": thumbnail_url,
                    "type": "thumbnail"
                })
            else:
                # Fallback to image_versions for thumbnail
                image_versions = post.get("image_versions", [])
                if image_versions:
                    media_list.append({
                        "url": image_versions[0].get("url"),
                        "type": "thumbnail"
                    })

        # Filter out any potential None values if URLs weren't found
        post_info["media_list"] = [media for media in media_list if media.get("url")]
        image_data = None
        post_info['media_bytes'] = {
            "type":"",
            "url":"",
            "image_bytes":None
        }
        for i, img_data in enumerate(post_info["media_list"]):
            image_data = sync_download_image(img_data["url"])
            if image_data:
                post_info["media_bytes"] = {
                    "type": img_data["type"],
                    "url": img_data["url"],
                    "image_bytes": image_data.read()
                }
                break
        
        extracted_posts.append(post_info)

    return extracted_posts



def get_latest_instagram_post(page_id:str, last_created_at: int = None, n_posts: int = 10) -> List[dict]:
    """
    Get latest Instagram posts for a given page.
    
    Args:
        page_name: Instagram username or ID
        last_created_at: Unix timestamp - only return posts after this time. If None, get latest n_posts
        n_posts: Maximum number of posts to return (default 10)
    
    Returns:
        List of extracted post dictionaries
    """
    pagination_token = None
    post_array = []
    should_continue = True

    query_string = {"amount":n_posts,"user_id":page_id}
    url = "https://instagram-premium-api-2023.p.rapidapi.com/v1/user/medias/chunk"
    headers = {"x-rapidapi-key": api_key, "x-rapidapi-host": "instagram-premium-api-2023.p.rapidapi.com"}

    while should_continue:
        if pagination_token:
            query_string["end_cursor"] = pagination_token

        data = call_rapid_api(url=url, params=query_string, headers=headers)
        if not data:
            return []

        posts = data[0]
        pagination_token = data[1]

        if posts:
            posts_info = extract_instagram_post_data(posts)
            
            # Filter posts based on timestamp if provided
            if last_created_at is not None:
                # Only include posts that are newer than the given timestamp
                filtered_posts = [post for post in posts_info if post["taken_at"] > last_created_at]
                post_array.extend(filtered_posts)
                
                # Check if we found any old posts (older than timestamp) - if so, we can stop
                old_posts_found = any(post["taken_at"] <= last_created_at for post in posts_info)
                if old_posts_found:
                    should_continue = False
            else:
                # No timestamp filtering, just add all posts
                post_array.extend(posts_info)

        # Stop conditions:
        # 1. If we have enough posts (n_posts limit reached)
        # 2. If no more pagination token available
        # 3. If we're filtering by timestamp and found old posts
        if len(post_array) >= n_posts:
            should_continue = False
        elif not pagination_token:
            should_continue = False

    # Limit to requested number of posts
    return post_array[:n_posts]


def extract_tweet_details(tweet_data: dict) -> dict:
    """
    Extracts key details from a tweet's JSON data, including user info,
    verification status, profile picture, text, media URLs, and quoted tweet data.
    
    For videos, it finds the highest bitrate MP4 URL.
    For photos, it uses the standard media URL.
    For quoted tweets, it extracts user info, text, media, and creation date.

    Args:
        tweet_data: A dictionary containing the full tweet data structure.

    Returns:
        A dictionary containing user details, verification status, text,
        media objects, and quoted tweet information if present. Returns a dictionary 
        with empty values if the data cannot be parsed.
    """
    extracted_info = {
        "username": None,
        "userhandle": None,
        "is_verified": False, # Default to False
        "profile_picture_url": None,
        "text": None,
        "media": [],
        "quoted_username": None,
        "quoted_userhandle": None,
        "quoted_is_verified": False,
        "quoted_profile_picture_url": None,
        "quoted_text": None,
        "quoted_media": [],
        "quoted_created_at": None
    }

    try:
        # Navigate through the nested JSON to the main result object
        tweet_result = tweet_data['result']['tweetResult']['result']
        user_result = tweet_result['core']['user_results']['result']
        # --- Extract User Info ---
        user_legacy = user_result['legacy']
        extracted_info['username'] = user_legacy.get('name')
        extracted_info['userhandle'] = user_legacy.get('screen_name')
        extracted_info['profile_picture_url'] = user_legacy.get('profile_image_url_https')
        
        # --- Extract Verification Status ---
        extracted_info['is_verified'] = user_result.get('is_blue_verified', False)

        # --- Extract Tweet Text ---
        extracted_info['text'] = tweet_result['legacy'].get('full_text')

        # --- Extract Media Details ---
        if 'extended_entities' in tweet_result['legacy']:

            media_list = tweet_result['legacy']['extended_entities'].get('media', [])

            for media_item in media_list:
                media_type = media_item.get('type')
                media_detail = {"type": media_type}

                # If it's a video or animated GIF, find the best video file
                if media_type in ['video', 'animated_gif']:
                    video_variants = media_item.get('video_info', {}).get('variants', [])
                    best_variant_url = None
                    max_bitrate = -1

                    for variant in video_variants:
                        if variant.get('content_type') == 'video/mp4':
                            bitrate = variant.get('bitrate', 0)
                            if bitrate > max_bitrate:
                                max_bitrate = bitrate
                                best_variant_url = variant.get('url')

                    media_detail['url'] = best_variant_url

                # If it's a photo, get the standard media URL
                elif media_type == 'photo':
                    media_detail['url'] = media_item.get('media_url_https')

                if media_detail.get('url'):
                    extracted_info['media'].append(media_detail)
        
        # --- Extract Quoted Tweet Data ---
        quoted_status = tweet_result.get("quoted_status_result", {}).get("result", {})
        if quoted_status:
            quoted_info = {
                "quoted_username": None,
                "quoted_userhandle": None,
                "quoted_is_verified": False,
                "quoted_profile_picture_url": None,
                "quoted_text": None,
                "quoted_media": [],
                "quoted_created_at": None
            }
            
            try:
                # Extract quoted user info
                quoted_user = quoted_status.get('core', {}).get('user_results', {}).get('result', {})
                if quoted_user:
                    quoted_user_legacy = quoted_user.get('legacy', {})
                    quoted_info["quoted_username"] = quoted_user_legacy.get('name')
                    quoted_info["quoted_userhandle"] = quoted_user_legacy.get('screen_name')
                    quoted_info["quoted_is_verified"] = quoted_user.get('is_blue_verified', False)
                    quoted_info["quoted_profile_picture_url"] = quoted_user_legacy.get('profile_image_url_https')
                
                # Extract quoted tweet text and creation date
                quoted_legacy = quoted_status.get('legacy', {})
                quoted_info["quoted_text"] = quoted_legacy.get('full_text')
                quoted_info["quoted_created_at"] = quoted_legacy.get('created_at')
                
                # Extract quoted tweet media
                if 'extended_entities' in quoted_legacy:
                    quoted_media_list = quoted_legacy['extended_entities'].get('media', [])
                    
                    for media_item in quoted_media_list:
                        media_type = media_item.get('type')
                        media_detail = {"type": media_type}

                        # If it's a video or animated GIF, find the best video file
                        if media_type in ['video', 'animated_gif']:
                            video_variants = media_item.get('video_info', {}).get('variants', [])
                            best_variant_url = None
                            max_bitrate = -1

                            for variant in video_variants:
                                if variant.get('content_type') == 'video/mp4':
                                    bitrate = variant.get('bitrate', 0)
                                    if bitrate > max_bitrate:
                                        max_bitrate = bitrate
                                        best_variant_url = variant.get('url')
                            
                            media_detail['url'] = best_variant_url

                        # If it's a photo, get the standard media URL
                        elif media_type == 'photo':
                            media_detail['url'] = media_item.get('media_url_https')
                        
                        if media_detail.get('url'):
                            quoted_info['quoted_media'].append(media_detail)
                
                # Add quoted info to main extracted_info
                extracted_info.update(quoted_info)
                
            except (KeyError, TypeError) as e:
                print(f"An error occurred while parsing quoted tweet data: {e}")
                # Continue without quoted tweet data if there's an error

    except (KeyError, TypeError) as e:
        print(f"An error occurred while parsing the tweet data: {e}")
        return {
            "username": None,
            "userhandle": None,
            "is_verified": False,
            "profile_picture_url": None,
            "text": None,
            "media": [],
            "quoted_username": None,
            "quoted_userhandle": None,
            "quoted_is_verified": False,
            "quoted_profile_picture_url": None,
            "quoted_text": None,
            "quoted_media": [],
            "quoted_created_at": None
        }
        
    return extracted_info


def get_tweet_data(tweet_url:str) -> dict:
    tweet_id = tweet_url.split("/")[-1]
    url = "https://twitter241.p.rapidapi.com/tweet-v2"
    query_string = {"pid": tweet_id}
    headers = {"x-rapidapi-key": api_key, "x-rapidapi-host": "twitter241.p.rapidapi.com"}
    data = call_rapid_api(url=url, params=query_string, headers=headers)
    return extract_tweet_details(data)

if __name__ == "__main__":
    # import json 
    # import pickle
    # with open("./data_/insta.json","r") as f:
    #     insta_data = json.load(f)
    # insta_data = insta_data[:10]
    # with open("./data_/insta_extracted.p","wb") as f:
    #     pickle.dump(get_latest_instagram_post(last_created_at=(datetime.now().timestamp() - 86400)),f)
    # import json
    # data = get_tweet_data("https://x.com/divyanshiwho/status/1962363623675707434")
    # with open("./data_/tweet_data.json","w") as f:
    #     json.dump(data,f,indent=4)

    import json
    with open("./data_/tweet_data.json","r") as f:
        data = json.load(f)
    print(data.keys())
    with open("./data_/tweet_data_extracted.json","w") as f:
        json.dump(extract_tweet_details(data),f,indent=4)
    