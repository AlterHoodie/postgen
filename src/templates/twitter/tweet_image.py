TEMPLATE_DESCRIPTION = """
Twitter Post: This template creates authentic-looking Twitter post images for social media content. It replicates the Twitter interface with user profile information, verified badge, three-dot menu, tweet text, and optional media attachments. The template is optimized for 1080x1350 dimensions and maintains Twitter's visual design language with proper spacing, typography, and UI elements.
The template includes customizable user information (name, handle, profile picture) and supports both text-only tweets and tweets with image attachments.
NOTE: Only one slide is required for this template.
"""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Twitter Post Slide:
  ### Attributes:
  - This creates a realistic Twitter post interface with user profile and tweet content.
  
  - user_name: The display name of the Twitter user (can include emojis)
    EX: "apsara", "kris kapoor's gf"
  
  - user_handle: The Twitter handle/username starting with @
    EX: "@apsarawrites", "@heyyasaiyaara"
  
  - tweet_text: The main tweet content/message
    EX: "when you choose the guy who makes you laugh", "me and who"
  - verified_badge: Whether to show the blue verified checkmark (use the VERIFIED_BADGE constant or empty string)

  ### Text Input:
    {{
      "name": "twitter_post",
      "image_description": "str",
      "text":{{
      "user_name": "str",
      "user_handle": "str", 
      "tweet_text": "str",
      "add_verified_badge": "True/False"
      }}
    }}

NOTE: 
- The template automatically includes Twitter UI elements like the three-dot menu and proper styling
- Profile picture should be square/circular format for best results
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

HEADLINE_SLIDE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Twitter Post Template</title>
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
        padding: 85px;
        box-sizing: border-box;

        display: flex;
        flex-direction: column;
        justify-content: center;
      }}

      .tweet-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
        padding-bottom: 10px;
      }}

      .header-left {{
        display: flex;
        align-items: center;
      }}

      .three-dots {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding-right: 30px;
        padding-bottom: 30px;
      }}

      .dot {{
        width: 8px;
        height: 8px;
        background-color: #c0c9c8;
        border-radius: 50%;
      }}

      .profile-pic {{
        width: 100px;
        height: 110px;
        border-radius: 50%;
        margin-right: 24px;
        object-fit: cover;
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

      .verified-badge {{
        width: 28px;
        height: 28px;
        background-color: #1d9bf0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }}

      .verified-badge::after {{
        content: "✓";
        color: white;
        font-size: 18px;
        font-weight: bold;
      }}

      .user-handle {{
        font-size: 32px;
        color: #536471;
      }}

      .tweet-content {{
        display: flex;
        flex-direction: column;
        min-height: 0;
      }}

      .tweet-text {{
        font-size: 42px;
        color: #0f1419;
        line-height: 1.3;
        margin: 15px 0 60px 0;
        word-wrap: break-word;
        flex-shrink: 0;
      }}

      .tweet-media {{
        border-radius: 24px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
      }}

      .tweet-image {{
        width: 100%;
        display: block;
        border-radius: 24px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="tweet-header">
        <div class="header-left">
          <img src="{profile_pic}" alt="Profile Picture" class="profile-pic" />
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
      <div class="tweet-content">
        {tweet_text}
        <div class="tweet-media">
          <img src="{background_image}" alt="Tweet Media" class="tweet-image" />
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
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Twitter Post Template</title>
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
        padding: 85px;
        box-sizing: border-box;

        display: flex;
        flex-direction: column;
        justify-content: center;
      }}

      .tweet-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-shrink: 0;
      }}

      .header-left {{
        display: flex;
        align-items: center;
      }}

      .three-dots {{
        display: flex;
        flex-direction: column;
        gap: 6px;
        padding-right: 30px;
        padding-bottom: 30px;
      }}

      .dot {{
        width: 8px;
        height: 8px;
        background-color: #c0c9c8;
        border-radius: 50%;
      }}

      .profile-pic {{
        width: 100px;
        height: 110px;
        border-radius: 50%;
        margin-right: 24px;
        object-fit: cover;
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

      .verified-badge {{
        width: 28px;
        height: 28px;
        background-color: #1d9bf0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }}

      .verified-badge::after {{
        content: "✓";
        color: white;
        font-size: 18px;
        font-weight: bold;
      }}

      .user-handle {{
        font-size: 32px;
        color: #536471;
      }}

      .tweet-content {{
        display: flex;
        flex-direction: column;
        align-items: stretch;
        min-height: 0;
      }}

      .tweet-text {{
        font-size: 42px;
        color: #0f1419;
        line-height: 1.3;
        word-wrap: break-word;
        flex-shrink: 0;
      }}

      .tweet-media {{
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
      }}

      .tweet-video {{
        width: 100%;
        display: block;
        object-fit: cover;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="tweet-header">
        <div class="header-left">
          <img src="{profile_pic}" alt="Profile Picture" class="profile-pic" />
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
      <div class="tweet-content">
          {tweet_text}
        <div class="tweet-media">
          <video src="{background_video}" alt="Tweet Media" class="tweet-video" />
        </div>
      </div>
    </div>
  </body>
</html>
"""

tweet_image_template = {
    "page_name": "twitter",
    "template_type": "tweet_image",
    "text_template": {"template_description":TEMPLATE_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "twitter_post": {
            "html_template": HEADLINE_SLIDE_HTML_TEMPLATE,
            "overlay_template": HEADLINE_SLIDE_OVERLAY_TEMPLATE,
            "text": {
                    "user_name": {"type": "text", "tag": "span", "class": ""},
                    "user_handle": {"type": "text", "tag": "span", "class": "user-handle"},
                    "tweet_text": {"type": "text_area", "tag": "p", "class": "tweet-text"},
                    "add_verified_badge": {"type": "checkbox", "html_snippet": VERIFIED_BADGE},
            },
            "assets":{
                "background_video": {"type":"bytes", "file_type":"mp4"},
                "background_image": {"type":"bytes", "file_type":"png"},
                "profile_pic": {"type":"bytes", "file_type":"png", "default": "profile_pic.png"},
            },
            "image_edits": {
            },
            "video_edits":{
                "type": {"type":"default", "values": "video_overlay"},
                "class_name":{"type":"default","values":"tweet-media"},
                "padding":{"type":"default","values":85},
            }
        },
    },
}