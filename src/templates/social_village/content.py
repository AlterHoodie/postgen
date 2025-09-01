TEMPLATE_DESCRIPTION = """
Content: This Social Village template creates engaging content slides for social media posts. It features a full-screen background image with centered text overlay that includes bold headlines with yellow highlighting capabilities. The design uses the Social Village logo and clean typography with shadow effects for optimal readability over images. Perfect for storytelling and content that needs to capture attention with minimal text.
NOTE: Only one slide is required for this template.
"""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Content Slide:
  ### Attributes:
  - This should be an engaging content slide for storytelling. Must have compelling visual and text.
    EX: A photo of a celebrity or relevant scene from entertainment/lifestyle content.
  
  - image_description: A one line description of the image you would like to use for the slide.
  - headline: The main headline content. Use **str** for highlighting important words and \n for line breaks.
    EX: **Badass Ravi Kumar** is my spirit animal
    Note: Use plain text with **str** for highlighting.

  ### Text Input:
    {{
      "name": "content_slide",
      "image_description": "str",
      "text": {{
      "headline": "str"
      }}
    }}

NOTE: 
- Use **str** to highlight words and make the headline more engaging. Use \n for line breaks.
- DO NOT COMPLICATE THE IMAGE DESCRIPTIONS, KEEP IT SIMPLE AND DIRECT.
- Focus on creating engaging, shareable content that works well with Social Village branding.
"""

CONTENT_SLIDE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title></title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Poppins", sans-serif;
        background-color: #f0f0f0;
      }}
      .container {{
        position: relative;
        width: 1080px;
        height: 1350px;
        margin: auto;
        overflow: hidden;
      }}
      .background-image {{
        width: 100%;
        height: 100%;
        display: block;
        /* 'cover' scales the image to fill the container, cropping sides or top/bottom as needed */
        object-fit: cover;
        /* Aligns the image. 'center' horizontally, and 25% from the top vertically to shift it up. */
        object-position: center 25%;
      }}
      .logo {{
        position: absolute;
        top: -50px;
        right: -50px;
        width: 250px;
        height: 250px;
      }}
      .text-overlay {{
        position: absolute;
        top: 60%;
        left: 0;
        right: 0;
        color: white;
        display: flex;
        flex-direction: column;
      }}

      .text-content {{
        width: 80%;
        align-self: center;
      }}
      .text-content h1 {{
        margin: 0 0 0 0;
        font-size: 60px;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        -webkit-text-stroke: 1px black;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
      }}
      .text-content h1 .yellow {{
        color: #f0c713;
      }}

    </style>
  </head>
  <body>
    <div class="container">
      <img src="{logo_image}" alt="Social Village Logo" class="logo" />
      <img src="{background_image}" class="background-image" />
      <div class="text-overlay">
        <div class="text-content">
          <h1>
            {headline}
          </h1>
        </div>
      </div>
    </div>
  </body>
</html>
"""

CONTENT_SLIDE_OVERLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title></title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Poppins", sans-serif;
        background-color: #f0f0f0;
      }}
      .container {{
        position: relative;
        width: 1080px;
        height: 1350px;
        margin: auto;
        overflow: hidden;
      }}
      .background-image {{
        width: 100%;
        height: 100%;
        display: block;
        /* 'cover' scales the image to fill the container, cropping sides or top/bottom as needed */
        object-fit: cover;
        /* Aligns the image. 'center' horizontally, and 25% from the top vertically to shift it up. */
        object-position: center 25%;
      }}
      .logo {{
        position: absolute;
        top: -50px;
        right: -50px;
        width: 250px;
        height: 250px;
      }}
      .text-overlay {{
        position: absolute;
        top: 60%;
        left: 0;
        right: 0;
        color: white;
        display: flex;
        flex-direction: column;
      }}

      .text-content {{
        width: 80%;
        align-self: center;
      }}
      .text-content h1 {{
        margin: 0 0 0 0;
        font-size: 60px;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        -webkit-text-stroke: 1px black;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
      }}
      .text-content h1 .yellow {{
        color: #f0c713;
      }}

    </style>
  </head>
  <body>
    <div class="container">
      <img src="{logo_image}" alt="Social Village Logo" class="logo" />
      <div class="text-overlay">
        <div class="text-content">
          <h1>
            {headline}
          </h1>
        </div>
      </div>
    </div>
  </body>
</html>
"""

content_template = {
    "page_name": "social_village",
    "template_type": "content",
    "text_template": {
        "template_description": TEMPLATE_DESCRIPTION,
        "json_description": JSON_DESCRIPTION
    },
    "slides": {
        "content_slide": {
            "html_template": CONTENT_SLIDE_HTML_TEMPLATE,
            "overlay_template": CONTENT_SLIDE_OVERLAY_TEMPLATE,
            "text": {
                    "headline": {"type": "text", "tag": "h1", "class": ""}
                },
            "assets":{
                "background_image": {"type":"bytes", "file_type":"png"},
                "background_video": {"type":"bytes", "file_type":"mp4"},
                "logo_image": {"type": "dropdown", "values": ["logo.png"], "default": "logo.png"},
            },
            "image_edits": {
            },
            "video_edits":{
                "type": {"type":"default", "values": "image_overlay"},
            }
        }
    }
}
