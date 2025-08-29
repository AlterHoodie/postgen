TEMPLATE_DESCRIPTION = """
Thumbnail: This ScoopWhoop template creates eye-catching thumbnail images for social media posts. It combines a striking background image with bold, highlighted text overlays to grab attention and drive engagement. The thumbnail should capture the essence of the story while remaining visually appealing and readable at smaller sizes.
The source should only be used if the post or the news is not from ScoopWhoop.
NOTE: Only one slide is required for this template.
"""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Thumbnail Slide:
  ### Attributes:
  - This should be the opening slide of the storyboard. Must be eye catching and engaging.
    EX: A photo of a temple and a gurdwara created inside a game.
  
  - image_description: A one line description of the image you would like to use for the slide.
  - headline: The main headline of the story must be given as an html H1 tag 
    EX: Meanwhile Sharvi, Kavita, Dinaz and Jasmine after pulling off Netflix level scam

  ### Text Input:
    {{
      "name": "headline_slide",
      "image_description": "str",
      "text":{{
      "headline": "str",
      }}
    }}

NOTE: 
- YOU CAN USE "**str**" to highlight words and to make the headline more engaging. Use \\n tags to break the text into multiple lines.
- DO NOT COMPLICATE THE IMAGE DESCRIPTIONS, KEEP IT SIMPLE AND DIRECT.
"""
MEME_UP_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Meme</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Golos Text", sans-serif;
        /* background-color: #000; */
      }}
      .container {{
        position: relative;
        width: 1080px;
        height: 1350px;
        margin: auto;
        overflow: hidden;
        background-color: #000;
      }}
      .contain {{
        width: 100%;
        height: 100%;
        /* display: block; */
        /* 'contain' shows entire image without cropping */
        object-fit: contain;
        /* Move image down using transform instead of object-position */
        transform: translateY(80px);
      }}
      .cover {{
        width: 100%;
        height: 100%;
        display: block;
        /* 'cover' scales the image to fill the container, cropping sides or top/bottom as needed */
        object-fit: cover;
        /* Aligns the image. 'center' horizontally, and 25% from the top vertically to shift it up. */
        /* object-position: center 25%; */
      }}
      .logo {{
        position: absolute;
        top: 50px;
        left: 60px;
        width: 125px;
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        /* top: 1050px; */
        top: 200px;
        left: 75px;
        right: 75px;
        color: white;
      }}
      .text-overlay h1 {{
        margin: 0;
        font-size: 3.2em;
        font-weight: 1000;
        /* line-height: 1.15; */
        text-align: center;
        -webkit-text-stroke: 2px black;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="{background_image}" class="{crop_type}" alt="test" />
      <img src="{logo_image}" alt="SW Logo" class="logo" />
      <div class="text-overlay">{headline}</div>
    </div>
  </body>
</html>
"""

MEME_UP_OVERLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Meme</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Golos Text", sans-serif;
        /* background-color: #000; */
      }}
      .container {{
        position: relative;
        width: 1080px;
        height: 1350px;
        margin: auto;
        overflow: hidden;
        background-color: #000;
      }}
      .crop {{
        width: 100%;
        height: 100%;
        /* display: block; */
        /* 'contain' shows entire image without cropping */
        object-fit: contain;
        /* Move image down using transform instead of object-position */
        transform: translateY(80px);
      }}
      .fill {{
        width: 100%;
        height: 100%;
        display: block;
        /* 'cover' scales the image to fill the container, cropping sides or top/bottom as needed */
        object-fit: cover;
        /* Aligns the image. 'center' horizontally, and 25% from the top vertically to shift it up. */
        /* object-position: center 25%; */
      }}
      .logo {{
        position: absolute;
        top: 50px;
        left: 60px;
        width: 125px;
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        /* top: 1050px; */
        top: 200px;
        left: 75px;
        right: 75px;
        color: white;
      }}
      .text-overlay h1 {{
        margin: 0;
        font-size: 3.2em;
        font-weight: 1000;
        /* line-height: 1.15; */
        text-align: center;
        -webkit-text-stroke: 2px black;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="{logo_image}" alt="SW Logo" class="logo" />
      <div class="text-overlay">{headline}</div>
    </div>
  </body>
</html>
"""

MEME_DOWN_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Meme</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Golos Text", sans-serif;
        /* background-color: #000; */
      }}
      .container {{
        position: relative;
        width: 1080px;
        height: 1350px;
        margin: auto;
        overflow: hidden;
        background-color: #000;
      }}
      .contain {{
        width: 100%;
        height: 100%;
        /* display: block; */
        /* 'contain' shows entire image without cropping */
        object-fit: contain;
        /* Move image down using transform instead of object-position */
        /* transform: translateY(-80px); */
      }}
      .cover {{
        width: 100%;
        height: 100%;
        display: block;
        /* 'cover' scales the image to fill the container, cropping sides or top/bottom as needed */
        object-fit: cover;
        /* Aligns the image. 'center' horizontally, and 25% from the top vertically to shift it up. */
        /* object-position: center 25%; */
      }}
      .logo {{
        position: absolute;
        top: 50px;
        left: 60px;
        width: 125px;
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        top: 1050px;
        /* top: 200px; */
        left: 75px;
        right: 75px;
        color: white;
      }}
      .text-overlay h1 {{
        margin: 0;
        font-size: 3.2em;
        font-weight: 1000;
        /* line-height: 1.15; */
        text-align: center;
        -webkit-text-stroke: 2px black;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="{background_image}" class="{crop_type}" alt="test" />
      <img src="{logo_image}" alt="SW Logo" class="logo" />
      <div class="text-overlay">{headline}</div>
    </div>
  </body>
</html>
"""

MEME_DOWN_OVERLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Meme</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Golos Text", sans-serif;
        /* background-color: #000; */
      }}
      .container {{
        position: relative;
        width: 1080px;
        height: 1350px;
        margin: auto;
        overflow: hidden;
        background-color: #000;
      }}
      .crop {{
        width: 100%;
        height: 100%;
        /* display: block; */
        /* 'contain' shows entire image without cropping */
        object-fit: contain;
        /* Move image down using transform instead of object-position */
        /* transform: translateY(-80px); */
      }}
      .fill {{
        width: 100%;
        height: 100%;
        display: block;
        /* 'cover' scales the image to fill the container, cropping sides or top/bottom as needed */
        object-fit: cover;
        /* Aligns the image. 'center' horizontally, and 25% from the top vertically to shift it up. */
        /* object-position: center 25%; */
      }}
      .logo {{
        position: absolute;
        top: 50px;
        left: 60px;
        width: 125px;
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        top: 1050px;
        /* top: 200px; */
        left: 75px;
        right: 75px;
        color: white;
      }}
      .text-overlay h1 {{
        margin: 0;
        font-size: 3.2em;
        font-weight: 1000;
        /* line-height: 1.15; */
        text-align: center;
        -webkit-text-stroke: 2px black;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="{logo_image}" alt="SW Logo" class="logo" />
      <div class="text-overlay">{headline}</div>
    </div>
  </body>
</html>
"""



meme_template = {
    "page_name": "scoopwhoop",
    "template_type": "meme",
    "text_template": {"template_description":TEMPLATE_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "meme_up_slide": {
            "html_template": MEME_UP_HTML_TEMPLATE,
            "overlay_template": MEME_UP_OVERLAY_TEMPLATE,
            "text": {
                "headline": {"type": "text", "tag": "h1", "class": ""},
            },
            "assets":{
                "background_video": {"type":"bytes", "file_type":"mp4"},
                "background_image": {"type":"bytes", "file_type":"png"},
                "logo_image": {"type": "dropdown", "values": ["logo.png","logo_original.png", "logo_hottake.png"], "default": "logo.png"},
            },
            "image_edits": {
                "crop_type": {"type": "dropdown", "values": ["cover", "contain"]},
            },
            "video_edits":{
                "type": {"type":"default", "values": "image_overlay"},
                "crop_type": {"type": "dropdown", "values": ["cover", "contain"]},
                "offset": {"type":"default", "values": 75},
                "add_gradient": {"type":"default", "values": False}
            }
        },
        "meme_down_slide": {
            "html_template": MEME_DOWN_HTML_TEMPLATE,
            "overlay_template": MEME_DOWN_OVERLAY_TEMPLATE,
            "text": {
                "headline": {"type": "text", "tag": "h1", "class": ""},
            },
            "assets":{
                "background_video": {"type":"bytes", "file_type":"mp4"},
                "background_image": {"type":"bytes", "file_type":"png"},
                "logo_image": {"type": "dropdown", "values": ["logo.png","logo_original.png", "logo_hottake.png"], "default": "logo.png"},
            },
            "image_edits": {
                "crop_type": {"type": "dropdown", "values": ["cover", "contain"]},
            },
            "video_edits":{
                "type": {"type":"default", "values": "image_overlay"},
                "crop_type": {"type": "dropdown", "values": ["cover", "contain"]},
                "offset": {"type":"default", "values": -50},
                "add_gradient": {"type":"default", "values": False}
            }
        },
    },
}
