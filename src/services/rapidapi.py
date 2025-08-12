import requests
import os 
from dotenv import load_dotenv
from typing import List

from src.clients import sync_download_image

load_dotenv(override=True)
api_key = os.getenv("RAPID_API_KEY")

headers = {"x-rapidapi-key": api_key, "x-rapidapi-host": "media-api4.p.rapidapi.com"}

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
        post_info["code"] = post["code"]
        post_info["taken_at"] = post["taken_at"]
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

        # 4. Played count (only for videos)
        if post_info["type"] == "video":
            # Use play_count if available, fallback to ig_play_count
            play_count = post.get("play_count")
            if play_count is None:
                play_count = post.get("ig_play_count")  # Check alternative key

            post_info["played_count"] = play_count if play_count is not None else 0
        else:
            post_info["played_count"] = None  # Not applicable for images/carousels

        # 5. Hashtags
        caption_data = post.get("caption")
        if caption_data and isinstance(caption_data, dict):
            post_info["hashtags"] = caption_data.get("hashtags", [])
            post_info["mentions"] = caption_data.get("mentions", [])
        else:
            post_info["hashtags"] = []
            post_info["mentions"] = []

        # 6. Is paid partnership
        post_info["is_paid_partnership"] = post.get("is_paid_partnership", False)

        # 7. Caption
        if caption_data and isinstance(caption_data, dict):
            post_info["caption"] = caption_data.get("text", "")
        else:
            post_info["caption"] = ""

        # 8. Media list (URLs and types)
        media_list = []
        if post_info["type"] == "carousel":
            carousel_items = post.get("carousel_media", [])
            for item in carousel_items:
                # Check if it's an image or video within the carousel
                if item.get("media_type") == 1:  # Image
                    image_versions = item.get("image_versions", {}).get("items", [])
                    if image_versions:
                        media_list.append({
                            "url": image_versions[0].get("url"),
                            "type": "image"
                        })
                elif item.get("media_type") == 2:  # Video
                    video_versions = item.get("video_versions", [])
                    if video_versions:
                        media_list.append({
                            "url": video_versions[0].get("url"),
                            "type": "video"
                        })

        elif post_info["type"] == "image":
            image_versions = post.get("image_versions", {}).get("items", [])
            if image_versions:
                media_list.append({
                    "url": image_versions[0].get("url"),
                    "type": "image"
                })

        elif post_info["type"] == "video":
            video_versions = post.get("video_versions", [])
            if video_versions:
                media_list.append({
                    "url": video_versions[0].get("url"),
                    "type": "video"
                })
            # Add thumbnail as well
            image_versions = post.get("image_versions", {}).get("items", [])
            if image_versions:
                media_list.append({
                    "url": image_versions[0].get("url"),
                    "type": "thumbnail"
                })

        # Filter out any potential None values if URLs weren't found
        post_info["media_list"] = [media for media in media_list if media["url"]]
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



def get_latest_instagram_post(page_name: str, last_created_at: int = None, n_posts: int = 10) -> List[dict]:
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

    query_string = {"username_or_id_or_url": page_name}
    url = "https://media-api4.p.rapidapi.com/v1/posts"

    while should_continue:
        if pagination_token:
            query_string["pagination_token"] = pagination_token

        data = call_rapid_api(url=url, params=query_string, headers=headers)
        if data.get("error"):
            return data

        posts = data["data"]["items"]

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
        elif not data.get("pagination_token"):
            should_continue = False
        else:
            pagination_token = data["pagination_token"]

    # Limit to requested number of posts
    return post_array[:n_posts]

if __name__ == "__main__":
    import time
    
    page_name = "scoopwhoop"
    
    # Test case 2: Get posts after a specific timestamp (e.g., 7 days ago)
    print("\n=== Test 2: Posts after timestamp ===")
    seven_days_ago = int(time.time()) - (2*60 * 60) # 7 days ago
    recent_posts = get_latest_instagram_post(page_name, last_created_at=seven_days_ago, n_posts=10)
    print(f"Found {len(recent_posts)}")
    
    if recent_posts:
        print(f"Most recent post timestamp: {recent_posts[0]['taken_at']}")
        print(f"Oldest post timestamp: {recent_posts[-1]['taken_at']}")