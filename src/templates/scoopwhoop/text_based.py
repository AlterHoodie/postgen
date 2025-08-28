TEXT_DESCRIPTION = """This ScoopWhoop template is perfect for creating viral social media content by presenting a bold or humorous "hot take." The main text grabs attention with a strong opinion, while the subtext offers a witty punchline or further explanation. Its simple, high-contrast design ensures the message is clear and instantly shareable, making it ideal for sparking conversation and engagement."""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Text Based Slide:
  - This template only one type of slide, Text Based Slide - it must be catchy, engaging and viral.
  - Note: Only one slide is required for this template.

  ### Attributes:
  
  - logo_image: The logo image to be used for the slide. For normal posts, use logo_1.png. For "hottakes", use logo_hottake.png
    EX: logo_1.png or logo_hottake.png
  - background_image: The background image to be used for the slide. For normal posts, use blue_background.png. For "hottakes", use black_background.png
    EX: blue_background.png or black_background.png
  - headline: The main headline of the story must be given as an html H1 tag 
    EX: IPL just doesn't seem that **exciting** anymore.
  - subtext: A short subtext for the post, one sentence max.
    Ex: And then I realized mummy hamesha last mai kyun khaati thi.
  ### Text Input:
    {{
      "name": "text_based_slide",
      "text":{{
      "headline": "str",
      "subtext": "str"
      }}
    }}

NOTE: 
- Use **str** to highlight parts of the text and \\n for new line.

"""

TEXT_BASED_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>IPL Excitement</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Golos Text", sans-serif;
        background-color: #f0f0f0;
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
      .container {{
        position: relative;
        width: 1080px;
        height: 1350px;
        margin: auto;
        overflow: hidden;
      }}
      .logo {{
        position: absolute;
        top: 220px;
        left: 140px;
        width: 280px;
        height: auto;
      }}
      /* Repurposing text-overlay as a centered container for the text content */
      .text-overlay {{
        position: absolute;
        top: 50%;
        left: 50%;
        width: 90%; /* Controls the text wrapping */
        transform: translate(-50%, -50%);
        color: white;
      }}
      /* Removed the blue-bar as it's not in the reference image */
      .text-content {{
        text-align: left;
        padding: 125px 25px 0 100px;
      }}
      .text-content h1 {{
        margin: 0;
        font-size: 4.5em;
        font-weight: 700;
        line-height: 1.15;
      }}
      .text-content h1 .yellow {{
        color: #ffdd00;
      }}
      .text-content .subtext {{
        margin: 20px 0 0;
        font-size: 3.5em;
        font-weight: 400;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="{logo_image}" alt="Scoop Whoop Logo" class="logo" />
      <img src="{background_image}" alt="Scoop Whoop Logo" class="background-image" />
      <div class="text-overlay">
        <div class="text-content">
          {headline}
          {subtext}
        </div>
      </div>
    </div>
  </body>
</html>
"""

text_based_template = {
    "page_name": "scoopwhoop",
    "template_type": "text_based",
    "text_template": {"template_description":TEXT_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "text_based_slide": {
            "html_template": TEXT_BASED_HTML_TEMPLATE,
            "overlay_template": "",
            "text": {
                "headline": {"type": "text", "tag": "h1", "class": ""},
                "subtext": {"type": "text", "tag": "p", "class": "subtext"},
            },
            "assets":{
                "logo_image": {"type": "dropdown", "values": ["logo_original.png", "logo_hottake.png"], "default": "logo_original.png"},
                "background_image": {"type": "dropdown", "values": ["blue_background.png", "black_background.png"], "default": "blue_background.png"},
            },
            ## No edits because background image not there
            "image_edits": {},
            "video_edits":{
                "type": {"type":"default", "values": "image_overlay"},
            }
        },
    },
}