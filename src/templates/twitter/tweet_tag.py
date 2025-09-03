TEMPLATE_DESCRIPTION = """
Twitter Tagged Post: This template creates authentic-looking Twitter quote tweet images for social media content. It replicates the Twitter interface showing a main tweet that quotes/tags another tweet within it. The template includes the main user's profile, their comment, and the quoted tweet embedded below with full Twitter UI elements including engagement metrics and action buttons.
The template is optimized for 1080x1350 dimensions and maintains Twitter's dark theme visual design language with proper spacing, typography, and authentic interaction elements.
NOTE: Only one slide is required for this template.
"""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Twitter Quote Tweet Slide:
  ### Attributes:
  - This creates a realistic Twitter quote tweet interface with main user and quoted tweet content.
  
  - main_user_name: The display name of the main Twitter user posting the quote tweet
    EX: "Divyanshi", "Tech Insider"
  
  - main_user_handle: The main user's Twitter handle/username starting with @
    EX: "@divyanshiwho", "@techinsider"
  
  - main_tweet_text: The main user's comment on the quoted tweet
    EX: "Does anyone else see Trump and Putin kissing here? 😥😭", "This is exactly what we needed!"
  
  - main_verified_badge: Whether the main user has a verified checkmark
  
  - quoted_user_name: The display name of the quoted tweet's author
    EX: "karl stole my sausage", "Breaking News"
  
  - quoted_user_handle: The quoted user's Twitter handle
    EX: "@userizzLonely", "@breakingnews"
  
  - quoted_tweet_text: The content of the quoted tweet
    EX: "Guys, look at the cake I made today.", "Major announcement coming soon"
  
  - quoted_date: The date of the quoted tweet
    EX: "Aug 31", "Sep 2"
  
  - post_time: The time and date of the main post
    EX: "9:25 AM · Sep 1, 2025"
  
  - views_count: Number of views on the post
    EX: "243.6K", "1.2M"
  
  - reply_count: Number of replies
    EX: "172", "1.5K"
  
  - retweet_count: Number of retweets
    EX: "531", "2.8K"
  
  - like_count: Number of likes
    EX: "9.9K", "45.2K"
  
  - bookmark_count: Number of bookmarks
    EX: "318", "892"

  ### Text Input:
    {{
      "name": "twitter_quote_post",
      "image_description": "str",
      "text":{{
        "main_user_name": "str",
        "main_user_handle": "str", 
        "main_tweet_text": "str",
        "main_verified_badge": "True/False",
        "quoted_user_name": "str",
        "quoted_user_handle": "str",
        "quoted_tweet_text": "str",
        "quoted_date": "str",
        "post_time": "str",
        "views_count": "str",
        "reply_count": "str",
        "retweet_count": "str",
        "like_count": "str",
        "bookmark_count": "str"
      }}
    }}

NOTE: 
- The template automatically includes Twitter UI elements like action buttons, engagement metrics, and proper dark theme styling
- Profile pictures should be square/circular format for best results
- Tweet text should be concise and engaging like real Twitter posts
- Use verified_badge only for accounts that should appear verified
- Engagement numbers can include K, M suffixes for large numbers
"""

VERIFIED_BADGE = """
<svg viewBox="0 0 22 22" aria-label="Verified account" role="img" class="w-5 h-5 fill-[#1d9bf0]">
    <g>
        <path d="M20.396 11c-.018-.646-.215-1.275-.57-1.816-.354-.54-.852-.972-1.438-1.246.223-.607.27-1.264.14-1.897-.131-.634-.437-1.218-.882-1.687-.47-.445-1.053-.75-1.687-.882-.633-.13-1.29-.083-1.897.14-.273-.587-.706-1.084-1.246-1.438-.54-.354-1.17-.551-1.816-.57-.647-.018-1.276.215-1.817.57-.54.354-.972.852-1.246 1.438-.608-.223-1.264-.27-1.898-.14-.634.13-.1218.437-1.687.882-.445.47-1.053.75-1.687.882-.131.633-.083 1.29.14 1.897.586.274 1.084.706 1.438 1.246.354.54.551 1.17.57 1.816.018.647-.215 1.276-.57 1.817-.354.54-.852.972-1.438 1.246-.223.607-.27 1.264-.14 1.897.13.634.437 1.218.882 1.687.47.445 1.053.75 1.687.882.633.13 1.29.083 1.897-.14.274.587.706 1.084 1.246 1.438.54.354 1.17.551 1.817.57.646.018 1.275-.215 1.816-.57.54-.354.972-.852 1.246-1.438.607.223 1.264.27 1.897.14.633-.131 1.218-.437 1.687-.882.445-.47.75-1.053.882-1.687.13-.633.083-1.29-.14-1.897.587-.273 1.084-.706 1.438-1.246.355-.54.552-1.17.57-1.816zM9.662 14.85l-3.42-3.42 1.414-1.414 1.994 1.994 4.518-4.518 1.414 1.414-5.932 5.932z"></path>
    </g>
</svg>
"""

HEADLINE_SLIDE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Quote Tweet Template</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            width: 1080px;
            height: 1350px;
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 85px;
            box-sizing: border-box;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Main Post Container -->
        <div class="bg-black text-[#e7e9ea] max-w-xl w-full border border-[#2f3336] rounded-2xl p-4">
            
            <!-- Post Header -->
            <div class="flex items-start">
                <!-- Profile Picture -->
                <div class="flex-shrink-0 mr-3">
                    <img class="w-12 h-12 rounded-full" src="{main_profile_pic}" alt="Main user profile picture">
                </div>

                <!-- Post Content -->
                <div class="w-full">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-1">
                            <span class="font-bold">{main_user_name}</span>
                            <!-- Verified Badge -->
                            {main_verified_badge}
                            <span class="text-[#71767b]">{main_user_handle}</span>
                        </div>
                        <!-- More Options Icon -->
                        <div class="text-[#71767b]">
                            <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M3 12c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm9 2c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm7 0c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"></path></g></svg>
                        </div>
                    </div>

                    <!-- Post Text -->
                    <p class="mt-1">{main_tweet_text}</p>

                    <!-- Quoted Post -->
                    <div class="mt-3 border border-[#2f3336] rounded-2xl">
                        <!-- Quoted Post Content -->
                        <div class="p-3">
                            <div class="flex items-center text-sm mb-1">
                                <img class="w-5 h-5 rounded-full mr-2" src="{quoted_profile_pic}" alt="Quoted user profile picture">
                                <span class="font-bold">{quoted_user_name}</span>
                                <span class="text-[#71767b] ml-1">{quoted_user_handle} · {quoted_date}</span>
                            </div>
                            <p class="text-sm">{quoted_tweet_text}</p>
                        </div>
                         <!-- Quoted Post Image -->
                        <img class="rounded-b-2xl w-full h-auto object-cover" src="{quoted_image}" alt="Quoted tweet image">
                    </div>

                    <!-- Post Footer Info -->
                    <div class="flex items-center text-sm text-[#71767b] mt-4 pb-4 border-b border-[#2f3336]">
                        <span>{post_time} ·</span>
                        <span class="font-bold text-[#e7e9ea] ml-1">{views_count}</span>
                        <span class="ml-1">Views</span>
                    </div>

                    <!-- Action Bar -->
                    <div class="flex justify-around items-center pt-3">
                        <!-- Reply -->
                        <div class="flex items-center text-[#71767b] text-sm group reply-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                 <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M14.046 2.242l-4.148-.01h-.002c-4.374 0-7.8 3.427-7.8 7.802 0 4.098 3.18 7.394 7.312 7.662v2.457c0 .414.336.75.75.75s.75-.336.75-.75v-2.457c.158-.003.316-.01.474-.015.316-.017.63-.04.94-.067.312-.03.622-.064.93-.1.036-.005.07-.01.106-.014.336-.04.67-.087 1-.137.33-.05.658-.103 1.003-.163.345-.06.69-.124 1.033-.193.344-.07.686-.142 1.024-.22.338-.078.673-.162 1-.25.328-.088.653-.18 1-.276l.004-.002c.346-.1.69-.204 1.03-.313.34-.11.678-.222 1.014-.34l.002-.002c.67-.234 1.32-.496 1.94-.782.62-.286 1.21-.6 1.77-1l.004-.002c.56-.4.97-.84 1.34-1.33.37-.49.68-1.02.91-1.58.23-.56.39-1.15.48-1.76.09-.61.12-1.25.12-1.91 0-4.374-3.427-7.8-7.8-7.8h-.002z"></path></g></svg>
                            </div>
                            <span class="text-count ml-1 transition-colors duration-200">{reply_count}</span>
                        </div>
                        
                        <!-- Retweet -->
                        <div class="flex items-center text-[#71767b] text-sm group retweet-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                 <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M23.77 15.67c-.292-.293-.767-.293-1.06 0l-2.22 2.22V7.65c0-2.068-1.683-3.75-3.75-3.75h-5.85c-.414 0-.75.336-.75.75s.336.75.75.75h5.85c1.24 0 2.25 1.01 2.25 2.25v10.24l-2.22-2.22c-.293-.293-.768-.293-1.06 0s-.294.768 0 1.06l3.5 3.5c.145.147.337.22.53.22s.383-.072.53-.22l3.5-3.5c.294-.292.294-.767 0-1.06zM.23 8.33c.292.293.767.293 1.06 0l2.22-2.22V16.35c0 2.068 1.683 3.75 3.75 3.75h5.85c.414 0 .75-.336.75-.75s-.336-.75-.75-.75h-5.85c-1.24 0-2.25-1.01-2.25-2.25V6.11l2.22 2.22c.293.293.768.293 1.06 0s.294-.768 0-1.06l-3.5-3.5c-.145-.147-.337-.22-.53-.22s-.383.072-.53.22l-3.5 3.5c-.294.292-.294.767 0 1.06z"></path></g></svg>
                            </div>
                            <span class="text-count ml-1 transition-colors duration-200">{retweet_count}</span>
                        </div>

                        <!-- Like -->
                        <div class="flex items-center text-[#71767b] text-sm group like-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M12 21.638h-.014C9.403 21.59 1.95 14.856 1.95 8.478c0-3.064 2.525-5.754 5.403-5.754 2.29 0 3.83 1.58 4.646 2.73.814-1.148 2.354-2.73 4.645-2.73 2.88 0 5.404 2.69 5.404 5.755 0 6.376-7.454 13.11-10.037 13.157H12z"></path></g></svg>
                            </div>
                            <span class="text-count ml-1 transition-colors duration-200">{like_count}</span>
                        </div>

                        <!-- Bookmark -->
                        <div class="flex items-center text-[#71767b] text-sm group bookmark-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                 <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M4 4.5C4 3.12 5.119 2 6.5 2h11C18.881 2 20 3.12 20 4.5v18.44l-8-5.71-8 5.71V4.5z"></path></g></svg>
                            </div>
                             <span class="text-count ml-1 transition-colors duration-200">{bookmark_count}</span>
                        </div>
                        
                        <!-- Share -->
                        <div class="flex items-center text-[#71767b] text-sm group share-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M12 2.59l5.7 5.7-1.41 1.42L13 6.41V16h-2V6.41l-3.3 3.3-1.41-1.42L12 2.59zM21 15l-.02 3.51c0 1.38-1.12 2.49-2.5 2.49H5.5C4.11 21 3 19.88 3 18.5V15h2v3.5c0 .28.22.5.5.5h12.98c.28 0 .5-.22.5-.5L19 15h2z"></path></g></svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

HEADLINE_SLIDE_OVERLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Twitter Quote Tweet Template - Video Overlay</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            width: 1080px;
            height: 1920px;
            background-color: #000000;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 85px;
            box-sizing: border-box;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Main Post Container -->
        <div class="bg-black text-[#e7e9ea] max-w-xl w-full border border-[#2f3336] rounded-2xl p-4">
            
            <!-- Post Header -->
            <div class="flex items-start">
                <!-- Profile Picture -->
                <div class="flex-shrink-0 mr-3">
                    <img class="w-12 h-12 rounded-full" src="{main_profile_pic}" alt="Main user profile picture">
                </div>

                <!-- Post Content -->
                <div class="w-full">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-1">
                            <span class="font-bold">{main_user_name}</span>
                            <!-- Verified Badge -->
                            {main_verified_badge}
                            <span class="text-[#71767b]">{main_user_handle}</span>
                        </div>
                        <!-- More Options Icon -->
                        <div class="text-[#71767b]">
                            <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M3 12c0-1.1.9-2 2-2s2 .9 2 2-.9 2-2 2-2-.9-2-2zm9 2c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm7 0c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2z"></path></g></svg>
                        </div>
                    </div>

                    <!-- Post Text -->
                    <p class="mt-1">{main_tweet_text}</p>

                    <!-- Quoted Post -->
                    <div class="mt-3 border border-[#2f3336] rounded-2xl">
                        <!-- Quoted Post Content -->
                        <div class="p-3">
                            <div class="flex items-center text-sm mb-1">
                                <img class="w-5 h-5 rounded-full mr-2" src="{quoted_profile_pic}" alt="Quoted user profile picture">
                                <span class="font-bold">{quoted_user_name}</span>
                                <span class="text-[#71767b] ml-1">{quoted_user_handle} · {quoted_date}</span>
                            </div>
                            <p class="text-sm">{quoted_tweet_text}</p>
                        </div>
                         <!-- Quoted Post Video -->
                        <video class="rounded-b-2xl w-full h-auto object-cover" src="{quoted_video}" autoplay muted loop></video>
                    </div>

                    <!-- Post Footer Info -->
                    <div class="flex items-center text-sm text-[#71767b] mt-4 pb-4 border-b border-[#2f3336]">
                        <span>{post_time} ·</span>
                        <span class="font-bold text-[#e7e9ea] ml-1">{views_count}</span>
                        <span class="ml-1">Views</span>
                    </div>

                    <!-- Action Bar -->
                    <div class="flex justify-around items-center pt-3">
                        <!-- Reply -->
                        <div class="flex items-center text-[#71767b] text-sm group reply-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                 <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M14.046 2.242l-4.148-.01h-.002c-4.374 0-7.8 3.427-7.8 7.802 0 4.098 3.18 7.394 7.312 7.662v2.457c0 .414.336.75.75.75s.75-.336.75-.75v-2.457c.158-.003.316-.01.474-.015.316-.017.63-.04.94-.067.312-.03.622-.064.93-.1.036-.005.07-.01.106-.014.336-.04.67-.087 1-.137.33-.05.658-.103 1.003-.163.345-.06.69-.124 1.033-.193.344-.07.686-.142 1.024-.22.338-.078.673-.162 1-.25.328-.088.653-.18 1-.276l.004-.002c.346-.1.69-.204 1.03-.313.34-.11.678-.222 1.014-.34l.002-.002c.67-.234 1.32-.496 1.94-.782.62-.286 1.21-.6 1.77-1l.004-.002c.56-.4.97-.84 1.34-1.33.37-.49.68-1.02.91-1.58.23-.56.39-1.15.48-1.76.09-.61.12-1.25.12-1.91 0-4.374-3.427-7.8-7.8-7.8h-.002z"></path></g></svg>
                            </div>
                            <span class="text-count ml-1 transition-colors duration-200">{reply_count}</span>
                        </div>
                        
                        <!-- Retweet -->
                        <div class="flex items-center text-[#71767b] text-sm group retweet-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                 <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M23.77 15.67c-.292-.293-.767-.293-1.06 0l-2.22 2.22V7.65c0-2.068-1.683-3.75-3.75-3.75h-5.85c-.414 0-.75.336-.75.75s.336.75.75.75h5.85c1.24 0 2.25 1.01 2.25 2.25v10.24l-2.22-2.22c-.293-.293-.768-.293-1.06 0s-.294.768 0 1.06l3.5 3.5c.145.147.337.22.53.22s.383-.072.53-.22l3.5-3.5c.294-.292.294-.767 0-1.06zM.23 8.33c.292.293.767.293 1.06 0l2.22-2.22V16.35c0 2.068 1.683 3.75 3.75 3.75h5.85c.414 0 .75-.336.75-.75s-.336-.75-.75-.75h-5.85c-1.24 0-2.25-1.01-2.25-2.25V6.11l2.22 2.22c.293.293.768.293 1.06 0s.294-.768 0-1.06l-3.5-3.5c-.145-.147-.337-.22-.53-.22s-.383.072-.53.22l-3.5 3.5c-.294.292-.294.767 0 1.06z"></path></g></svg>
                            </div>
                            <span class="text-count ml-1 transition-colors duration-200">{retweet_count}</span>
                        </div>

                        <!-- Like -->
                        <div class="flex items-center text-[#71767b] text-sm group like-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M12 21.638h-.014C9.403 21.59 1.95 14.856 1.95 8.478c0-3.064 2.525-5.754 5.403-5.754 2.29 0 3.83 1.58 4.646 2.73.814-1.148 2.354-2.73 4.645-2.73 2.88 0 5.404 2.69 5.404 5.755 0 6.376-7.454 13.11-10.037 13.157H12z"></path></g></svg>
                            </div>
                            <span class="text-count ml-1 transition-colors duration-200">{like_count}</span>
                        </div>

                        <!-- Bookmark -->
                        <div class="flex items-center text-[#71767b] text-sm group bookmark-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                 <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M4 4.5C4 3.12 5.119 2 6.5 2h11C18.881 2 20 3.12 20 4.5v18.44l-8-5.71-8 5.71V4.5z"></path></g></svg>
                            </div>
                             <span class="text-count ml-1 transition-colors duration-200">{bookmark_count}</span>
                        </div>
                        
                        <!-- Share -->
                        <div class="flex items-center text-[#71767b] text-sm group share-group cursor-pointer">
                            <div class="icon-container p-2 rounded-full transition-colors duration-200">
                                <svg viewBox="0 0 24 24" aria-hidden="true" class="w-5 h-5 fill-current"><g><path d="M12 2.59l5.7 5.7-1.41 1.42L13 6.41V16h-2V6.41l-3.3 3.3-1.41-1.42L12 2.59zM21 15l-.02 3.51c0 1.38-1.12 2.49-2.5 2.49H5.5C4.11 21 3 19.88 3 18.5V15h2v3.5c0 .28.22.5.5.5h12.98c.28 0 .5-.22.5-.5L19 15h2z"></path></g></svg>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

tweet_tag_template = {
    "page_name": "twitter",
    "template_type": "tweet_tag",
    "text_template": {"template_description":TEMPLATE_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "twitter_quote_post": {
            "html_template": HEADLINE_SLIDE_HTML_TEMPLATE,
            "overlay_template": HEADLINE_SLIDE_OVERLAY_TEMPLATE,
            "text_only": False,
            "text": {
                    "main_user_name": {"type": "text", "tag": "span", "class": "font-bold"},
                    "main_user_handle": {"type": "text", "tag": "span", "class": "text-[#71767b]"},
                    "main_tweet_text": {"type": "text_area", "tag": "p", "class": "mt-1"},
                    "main_verified_badge": {"type": "checkbox", "html_snippet": VERIFIED_BADGE},
                    "quoted_user_name": {"type": "text", "tag": "span", "class": "font-bold"},
                    "quoted_user_handle": {"type": "text", "tag": "span", "class": "text-[#71767b] ml-1"},
                    "quoted_tweet_text": {"type": "text_area", "tag": "p", "class": "text-sm"},
                    "quoted_date": {"type": "text", "tag": "span", "class": "text-[#71767b] ml-1"},
                    "post_time": {"type": "text", "tag": "span", "class": ""},
                    "views_count": {"type": "text", "tag": "span", "class": "font-bold text-[#e7e9ea] ml-1"},
                    "reply_count": {"type": "text", "tag": "span", "class": "ml-1"},
                    "retweet_count": {"type": "text", "tag": "span", "class": "ml-1"},
                    "like_count": {"type": "text", "tag": "span", "class": "ml-1"},
                    "bookmark_count": {"type": "text", "tag": "span", "class": "ml-1"},
            },
            "assets":{
                "quoted_video": {"type":"bytes", "file_type":"mp4"},
                "quoted_image": {"type":"bytes", "file_type":"png"},
                "main_profile_pic": {"type":"bytes", "file_type":"png", "default": "profile_pic.png"},
                "quoted_profile_pic": {"type":"bytes", "file_type":"png", "default": "profile_pic.png"},
            },
            "image_edits": {
            },
            "video_edits":{
                "type": {"type":"default", "values": "video_overlay"},
                "class_name":{"type":"default","values":"quoted-video"},
                "padding":{"type":"default","values":85},
            }
        },
    },
}
