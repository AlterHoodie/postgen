TEMPLATE_DESCRIPTION = """
Thumbnail: This Social Village template creates eye-catching thumbnail images for social media posts. It combines a striking background image with bold, highlighted text overlays featuring a prominent headline and optional subtext. The design uses a dark gradient overlay at the bottom for text readability and includes the Social Village logo in the top-right corner. The thumbnail should capture the essence of the story while remaining visually appealing and readable at smaller sizes.
NOTE: Only one slide is required for this template.
"""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Thumbnail Slide:
  ### Attributes:
  - This should be the opening slide of the storyboard. Must be eye catching and engaging.
    EX: A photo of actors in a romantic scene from a movie.
  
  - image_description: A one line description of the image you would like to use for the slide.
  - headline: The main headline of the story. Use **str** for highlighting important words and \n for line breaks.
    EX: **Actors and Their First Heroine** On-Screen Still Didn't Fail To Serve The Chemistry
  
  - subtext: A short text for navigation or call-to-action, typically "Swipe >>" or similar.
    Ex: Swipe >>
  
  ### Text Input:
    {{
      "name": "headline_slide",
      "image_description": "str",
      "text": {{
      "headline": "str",
      "subtext": "str"
      }}
    }}

NOTE: 
- Use **str** to highlight words and make the headline more engaging. Use \n for line breaks.
- DO NOT COMPLICATE THE IMAGE DESCRIPTIONS, KEEP IT SIMPLE AND DIRECT.
- Subtext is typically a simple navigation prompt like "Swipe >>" or brief call-to-action.
"""


THUMBNAIL_SLIDE_HTML_TEMPLATE = """<!DOCTYPE html>
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
        object-fit: cover;
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
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.9) 0%,
          rgba(0, 0, 0, 0.8) 30%,
          rgba(0, 0, 0, 0.6) 50%,
          transparent 100%
        );
        padding: 60px 40px 35px 40px;
        color: white;
        display: flex;
        flex-direction: column;
      }}
      .text-content {{
        width: 100%;
      }}
      .text-content h1 {{
        margin: 0 0 0 0;
        font-size: 60px;
        font-weight: 600;
        line-height: 1;
        text-align: center;
        /* -webkit-text-stroke: 1px black; */
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
      }}
      .text-content h1 .yellow {{
        color: #f0c713;
      }}

      .text-content .subtext {{
        margin: 20px 0 0;
        font-size: 40px;
        font-weight: 600;
        text-align: center;
        -webkit-text-stroke: 1px black;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
        /* text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.8); */
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="{logo_path}" alt="Social Village Logo" class="logo" />
      <img src="{background_image}" class="background-image" />
      <div class="text-overlay">
        <div class="text-content">
          <h1>
            {headline}
          </h1>
          <div class="subtext">{subtext}</div>
        </div>
      </div>
    </div>
  </body>
</html>
"""

THUMBNAIL_SLIDE_OVERLAY_TEMPLATE = """<!DOCTYPE html>
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
        object-fit: cover;
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
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.9) 0%,
          rgba(0, 0, 0, 0.8) 30%,
          rgba(0, 0, 0, 0.6) 50%,
          transparent 100%
        );
        padding: 60px 40px 35px 40px;
        color: white;
        display: flex;
        flex-direction: column;
      }}
      .text-content {{
        width: 100%;
      }}
      .text-content h1 {{
        margin: 0 0 0 0;
        font-size: 60px;
        font-weight: 600;
        line-height: 1;
        text-align: center;
        /* -webkit-text-stroke: 1px black; */
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
      }}
      .text-content h1 .yellow {{
        color: #f0c713;
      }}

      .text-content .subtext {{
        margin: 20px 0 0;
        font-size: 40px;
        font-weight: 600;
        text-align: center;
        -webkit-text-stroke: 1px black;
        text-shadow: 4px 4px 8px rgba(0, 0, 0, 1);
        /* text-shadow: 4px 4px 8px rgba(0, 0, 0, 0.8); */
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="{logo_path}" alt="Social Village Logo" class="logo" />
      <div class="text-overlay">
        <div class="text-content">
          <h1>
            {headline}
          </h1>
          <div class="subtext">{subtext}</div>
        </div>
      </div>
    </div>
  </body>
</html>
"""

thumbnail_template = {
    "page_name": "social_village",
    "template_type": "thumbnail",
    "text_template": {"template_description":TEMPLATE_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "headline_slide": {
            "html_template": THUMBNAIL_SLIDE_HTML_TEMPLATE,
            "overlay_template": THUMBNAIL_SLIDE_OVERLAY_TEMPLATE,
            "text": {
                    "headline": {"type": "text", "tag": "h1", "class": ""},
                    "subtext": {"type": "text", "tag": "p", "class": "subtext"},
            },
            "assets":{
                "background_video": {"type":"bytes", "file_type":"mp4"},
                "background_image": {"type":"bytes", "file_type":"png"},
                "logo_image": {"type": "dropdown", "values": ["logo.png"], "default": "logo.png"},
            },
            "image_edits": {
                "crop_type": {"type": "dropdown", "values": ["cover", "contain"]},
            },
            "video_edits":{
                "type": {"type":"default", "values": "image_overlay"},
                "crop_type": {"type": "dropdown", "values": ["cover", "contain"]},
            }
        },
    },
}