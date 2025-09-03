from datetime import datetime


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
      }}
    }}

NOTE: 
- The template automatically includes Twitter UI elements like action buttons, engagement metrics, and proper dark theme styling
- Profile pictures should be square/circular format for best results
- Tweet text should be concise and engaging like real Twitter posts
- Use verified_badge only for accounts that should appear verified
"""

VERIFIED_BADGE = """
<svg
                xmlns="http://www.w3.org/2000/svg"
                xmlns:xlink="http://www.w3.org/1999/xlink"
                version="1.1"
                width="28"
                height="28"
                viewBox="0 0 256 256"
                xml:space="preserve"
              >
                <g
                  style="
                    stroke: none;
                    stroke-width: 0;
                    stroke-dasharray: none;
                    stroke-linecap: butt;
                    stroke-linejoin: miter;
                    stroke-miterlimit: 10;
                    fill: none;
                    fill-rule: nonzero;
                    opacity: 1;
                  "
                  transform="translate(1.4065934065934016 1.4065934065934016) scale(2.81 2.81)"
                >
                  <path
                    d="M 30.091 10.131 L 30.091 10.131 c 5.28 -13.046 23.695 -13.207 29.202 -0.255 l 0 0 l 0 0 c 12.959 -5.491 26.093 7.416 20.829 20.469 l 0 0 l 0 0 c 13.046 5.28 13.207 23.695 0.255 29.202 l 0 0 l 0 0 c 5.491 12.959 -7.416 26.093 -20.469 20.829 l 0 0 l 0 0 c -5.28 13.046 -23.695 13.207 -29.202 0.255 l 0 0 l 0 0 C 17.748 86.122 4.613 73.215 9.878 60.162 l 0 0 l 0 0 C -3.169 54.881 -3.33 36.467 9.623 30.96 l 0 0 l 0 0 C 4.131 18.001 17.038 4.866 30.091 10.131 L 30.091 10.131 z"
                    style="
                      stroke: none;
                      stroke-width: 1;
                      stroke-dasharray: none;
                      stroke-linecap: butt;
                      stroke-linejoin: miter;
                      stroke-miterlimit: 10;
                      fill: rgb(0, 150, 241);
                      fill-rule: nonzero;
                      opacity: 1;
                    "
                    transform=" matrix(1 0 0 1 0 0) "
                    stroke-linecap="round"
                  />
                  <polygon
                    points="39.66,63.79 23.36,47.76 28.97,42.05 39.3,52.21 59.6,29.58 65.56,34.93 "
                    style="
                      stroke: none;
                      stroke-width: 1;
                      stroke-dasharray: none;
                      stroke-linecap: butt;
                      stroke-linejoin: miter;
                      stroke-miterlimit: 10;
                      fill: rgb(255, 255, 255);
                      fill-rule: nonzero;
                      opacity: 1;
                    "
                    transform="  matrix(1 0 0 1 0 0) "
                  />
                </g>
              </svg>
"""

TWEET_TAG_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Twitter Quote Tweet Template</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
      rel="stylesheet"
    />
    <style>
      body,
      html {{
        margin: 0;
        padding: 0;
        font-family: "Inter", sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
      }}

      .container {{
        width: 1080px;
        height: 1350px;
        background-color: #ffffff;
        padding: 75px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }}

      /* Main tweet styling */
      .tweet {{
        display: flex;
        flex-direction: column;
        min-height: 0;
        align-items: center;
        width: 100%;
      }}

      .header-left {{
        display: flex;
        align-items: center;
      }}

      .profile-pic {{
        width: 100px;
        height: 110px;
        border-radius: 50%;
        margin-right: 24px;
        object-fit: cover;
        flex-shrink: 0;
      }}

      .tweet-body {{
        flex: 1;
      }}

      .tweet-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
        padding-bottom: 10px;
      }}

      .user-info {{     
        display: flex;
        flex-direction: column;
        line-height: 1.2;
      }}

      .user-name {{
        font-weight: 700;
        font-size: 36px;
        color: #0f1419;
        display: flex;
        align-items: center;
        gap: 8px;
      }}

      .user-handle {{
        font-size: 32px;
        color: #536471;
      }}

      .tweet-text {{
        font-size: 30px;
        color: #0f1419;
        line-height: 1.3;
        margin: 15px 0 20px 0;

        word-wrap: break-word;
        flex-shrink: 0;
      }}
      .tweet-footer {{
        font-size: 28px;
        color: #536471;
        line-height: 1.3;
        margin: 25px 0 20px 0;
        word-wrap: break-word;
        flex-shrink: 0;
        font-weight: 400;
        letter-spacing: 0.2px;
        padding: 0 4px;
      }}

      .tweet-footer .timestamp {{
        font-weight: 500;
        color: #536471;
      }}

      .tweet-footer .views {{
        font-weight: 600;
        color: #536471;
      }}

      .three-dots {{
        display: flex;
        flex-direction: column;
        justify-content: right;
        align-items: center;
        gap: 6px;
        padding-right: 20px;
        padding-bottom: 20px;
      }}

      .dot {{
        width: 8px;
        height: 8px;
        background-color: #c0c9c8;
        border-radius: 50%;
      }}

      /* Quoted tweet styling */
      .quoted-tweet {{
        height: auto;
        width: 100%;
        border-radius: 20px;
        border: 1px solid #e1e8ed;
        overflow: hidden;
      }}

      .quoted-header {{ 
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: none;
        border-radius: 20px 20px 0px 0px;
        padding: 18px 18px 4px 18px;
        font-size: 16px;
      }}

      .quoted-profile-pic {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
      }}

      .quoted-user-name {{
        font-size: 28px;
        font-weight: 600;
        color: #0f1419;
        margin-left: 8px;
      }}

      .quoted-user-handle {{
        font-size: 28px;
        color: #536471;
      }}

      .quoted-text {{
        font-size: 28px;
        color: #0f1419;
        line-height: 1.3;
        padding: 3px 18px 30px 18px;
      }}

      .quoted-image {{
        width: 100%;
        height: auto;
        object-fit: cover;
        display: block;
        border-radius: 0 0 16px 16px;
      }}
      .quoted-image.contain {{  
        width: auto;
        height: auto;
        object-fit: cover;
        display: block;
        border-radius: 0 0 20px 20px;
      }}

      /* Tweet media styling similar to reference */
      .tweet-media {{
        border-radius: 24px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
      }}

      .tweet-media.cover {{
        height: auto;
        width: 100%;
      }}

      .tweet-image {{
        width: 100%;
        height: auto;
        object-fit: cover;
        display: block;
        border-radius: 24px;
      }}

      .tweet-image.contain {{
        object-fit: contain;
        width: auto;
        height: 100%;
      }}

      .tweet-image.cover {{
        object-fit: cover;
        width: 100%;
        height: 100%;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="tweet-header">
        <div class="header-left">
          <img
            src="{profile_pic}"
            alt="Profile Picture"
            class="profile-pic"
          />
          <div class="user-info">
            <span class="user-name">
            {user_name}
            {add_verified_badge}
            </span>
            {user_handle}
          </div>
        </div>
        <div class="three-dots">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>
      <div class="tweet">
          {tweet_text}
        <div class="quoted-tweet">
          <div class="quoted-header">
            <img
              class="quoted-profile-pic"
              src="{quoted_profile_pic}"
              alt="Quoted user profile picture"
            />
            {quoted_user_name}
            {quoted_user_handle} · {quoted_date}
          </div>
          {quoted_tweet_text}
          <img class="quoted-image" src="{background_image}" alt="Quoted tweet image" />
        </div>
      </div>
    </div>
  </body>
  <script>
    // Global crop type - change this to 'contain' or 'cover'
    const CROP_TYPE = "{crop_type}"; // Change to 'cover' to test different behavior

    function alignWidths() {{
      const tweetImage = document.querySelector(".tweet-image");
      const quotedImage = document.querySelector(".quoted-image");
      const quotedTweet = document.querySelector(".quoted-tweet");
      const tweetHeader = document.querySelector(".tweet-header");
      const tweetText = document.querySelector(".tweet-text");

      // Determine which media element exists
      const mediaElement = tweetImage || quotedImage;

      if (mediaElement && tweetHeader && tweetText) {{
        // Apply crop type class to image and media container
        if (quotedImage) {{ 
          quotedImage.className = `quoted-image ${{CROP_TYPE}}`;
        }}

        if (CROP_TYPE === "contain") {{
          // For contain mode: align widths based on image dimensions (current behavior)
          function setWidths() {{
            const mediaWidth = mediaElement.offsetWidth;
            quotedTweet.style.width = mediaWidth + "px";
            tweetHeader.style.width = mediaWidth + "px";
            tweetText.style.width = mediaWidth + "px";
          }}

          // Handle different media types
          if (quotedImage) {{
            // For images
            if (quotedImage.complete && quotedImage.naturalWidth > 0) {{
              setWidths();
            }} else {{
              quotedImage.onload = setWidths;
            }}
          }}
        }} else if (CROP_TYPE === "cover") {{
          // For cover mode: image fills container, header and text use full container width
          const containerWidth =
            document.querySelector(".container").offsetWidth - 170; // Account for padding
          tweetHeader.style.width = containerWidth + "px";
          tweetText.style.width = containerWidth + "px";
        }}
      }}
    }}

    // Run when DOM is loaded
    document.addEventListener("DOMContentLoaded", alignWidths);

    // Run when window is resized (in case of responsive changes)
    window.addEventListener("resize", alignWidths);
  </script>
</html>
"""

TWEET_TAG_OVERLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Twitter Quote Tweet Template</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap"
      rel="stylesheet"
    />
    <style>
      body,
      html {{
        margin: 0;
        padding: 0;
        font-family: "Inter", sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
      }}

      .container {{
        width: 1080px;
        height: 1920px;
        background-color: #ffffff;
        padding: 75px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
      }}

      /* Main tweet styling */
      .tweet {{
        display: flex;
        flex-direction: column;
        min-height: 0;
        align-items: center;
        width: 100%;
      }}

      .header-left {{
        display: flex;
        align-items: center;
      }}

      .profile-pic {{
        width: 100px;
        height: 110px;
        border-radius: 50%;
        margin-right: 24px;
        object-fit: cover;
        flex-shrink: 0;
      }}

      .tweet-body {{
        flex: 1;
      }}    

      .tweet-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
        padding-bottom: 10px;
        width: 100%;
      }}

      .user-info {{
        display: flex;
        flex-direction: column;
        line-height: 1.2;
      }}

      .user-name {{
        font-weight: 700;
        font-size: 36px;
        color: #0f1419;
        display: flex;
        align-items: center;
        gap: 8px;
      }}

      .user-handle {{
        font-size: 32px;
        color: #536471;
      }}

      .tweet-text {{
        font-size: 30px;
        color: #0f1419;
        line-height: 1.3;
        margin: 15px 0 20px 0;
        width: 100%;
        text-align: left;
        word-wrap: break-word;
        flex-shrink: 0;
      }}
      .tweet-footer {{
        font-size: 28px;
        color: #536471;
        line-height: 1.3;
        margin: 25px 0 20px 0;
        word-wrap: break-word;
        flex-shrink: 0;
        font-weight: 400;
        letter-spacing: 0.2px;
        padding: 0 4px;
      }}

      .tweet-footer .timestamp {{
        font-weight: 500;
        color: #536471;
      }}

      .tweet-footer .views {{
        font-weight: 600;
        color: #536471;
      }}

      .three-dots {{
        display: flex;
        flex-direction: column;
        justify-content: right;
        align-items: center;
        gap: 6px;
        padding-right: 20px;
        padding-bottom: 20px;
      }}

      .dot {{
        width: 8px;
        height: 8px;
        background-color: #c0c9c8;
        border-radius: 50%;
      }}

      /* Quoted tweet styling */
      .quoted-tweet {{
        height: auto;
        width: 100%;
        border: 1px solid #e1e8ed;
        border-radius: 20px;
        overflow: hidden;
      }}

      .quoted-header {{
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: none;
        border-radius: 20px 20px 0px 0px;
        padding: 18px 18px 4px 18px;
        font-size: 16px;
      }}

      .quoted-profile-pic {{
        width: 60px;
        height: 60px;
        border-radius: 50%;
        object-fit: cover;
      }}

      .quoted-user-name {{
        font-size: 28px;
        font-weight: 600;
        color: #0f1419;
        margin-left: 8px;
      }}

      .quoted-user-handle {{
        font-size: 28px;
        color: #536471;
      }}

      .quoted-text {{
        font-size: 28px;
        color: #0f1419;
        line-height: 1.3;
        padding: 3px 18px 30px 18px;
      }}

      .quoted-video {{
        width: 100%;
        height: auto;
        object-fit: cover;
        display: block;
        border-radius: 0 0 16px 16px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="tweet-header">
        <div class="header-left">
          <img
            src="{profile_pic}"
            alt="Profile Picture"
            class="profile-pic"
          />
          <div class="user-info">
          <span class="user-name">
            {user_name}
            {add_verified_badge}
          </span>
            {user_handle}
          </div>
        </div>
        <div class="three-dots">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>
      <div class="tweet">
          {tweet_text}
        <div class="quoted-tweet">
          <div class="quoted-header">
            <img
              class="quoted-profile-pic"
              src="{quoted_profile_pic}"
              alt="Quoted user profile picture"
            />
            {quoted_user_name}
            {quoted_user_handle} · {quoted_date}
          </div>
          {quoted_tweet_text}
          <video class="quoted-video" src="{background_video}" alt="Quoted tweet image" />
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
            "html_template": TWEET_TAG_HTML_TEMPLATE,
            "overlay_template": TWEET_TAG_OVERLAY_TEMPLATE,
            "text_only": False,
            "text": {
                    "user_name": {"type": "text", "tag": "span", "class": ""},
                    "user_handle": {"type": "text", "tag": "span", "class": "user-handle"},
                    "tweet_text": {"type": "text_area", "tag": "div", "class": "tweet-text"},
                    "add_verified_badge": {"type": "checkbox", "html_snippet": VERIFIED_BADGE},
                    "quoted_user_name": {"type": "text", "tag": "span", "class": "quoted-user-name"},
                    "quoted_user_handle": {"type": "text", "tag": "span", "class": "quoted-user-handle"},
                    "quoted_tweet_text": {"type": "text_area", "tag": "div", "class": "quoted-text"},
                    "quoted_date": {"type": "text", "tag": "span", "class": "quoted-user-handle"},
            },
            "assets":{
                "background_video": {"type":"bytes", "file_type":"mp4"},
                "background_image": {"type":"bytes", "file_type":"png"},
                "profile_pic": {"type":"bytes", "file_type":"png", "default": "profile_pic.png"},
                "quoted_profile_pic": {"type":"bytes", "file_type":"png", "default": "profile_pic.png"},
            },
            "image_edits": {
                "crop_type":{"type":"dropdown", "values":["cover", "contain"], "default":"cover"},
            },
            "video_edits":{
                "type": {"type":"default", "values": "video_overlay"},
                "class_name":{"type":"default","values":"quoted-video"},
                "padding":{"type":"default","values":105},
            }
        },
    },
}
