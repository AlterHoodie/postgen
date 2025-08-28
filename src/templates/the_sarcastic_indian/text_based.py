TEXT_DESCRIPTION = """This ScoopWhoop template is perfect for creating viral social media content by presenting a bold or humorous "hot take." The main text grabs attention with a strong opinion, while the subtext offers a witty punchline or further explanation. Its simple, high-contrast design ensures the message is clear and instantly shareable, making it ideal for sparking conversation and engagement."""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Text Based Slide:
  - This template only one type of slide, Text Based Slide - it must be catchy, engaging and viral.
  - Note: Only one slide is required for this template.

  ### Attributes:
  - headline: The main headline of the story. Use **str** for highlighting important words and \n for line breaks.
    EX: IPL just doesn't seem that **exciting** anymore.
  - subtext: A short description for the post, one sentence max. Use plain text only.
    Ex: And then I realized mummy hamesha last mai kyun khaati thi.
  ### Text Input:
    {{
      "name": "text_based_slide",
      "text": {{
      "headline": "str",
      "subtext": "str"
      }}
    }}

"""


TEXT_BASED_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>The Sarcastic Indian</title>
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
        background-color: #f0f0f0;
      }}

      .container {{
        width: 1080px;
        height: 1350px;
        background-image: url("{background_image}");
        background-size: cover;
        background-position: center;
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        color: white;
        box-sizing: border-box;
        padding: 85px;
      }}

      .logo {{
        position: absolute;
        top: -40px;
        left: 10px;
        width: 270px;
      }}

      .headline {{
        font-size: 90px;
        font-weight: 700;
        line-height: 1.3;
        text-align: left;
        width: 100%;
      }}

      .swipe {{
        position: absolute;
        bottom: 0px;
        right: 55px;
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 20px;
      }}

      .source {{
        position: absolute;
        bottom: 0px;
        left: 20px;
        font-size: 25px;
        font-style: italic;
        font-weight: 500; /* Regular weight */
        margin-bottom: 20px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
        {headline}
        {news_source}
      <p class="swipe">Swipe>>></p>
    </div>
  </body>
</html>
"""

text_based_template = {
    "page_name": "the_sarcastic_indian",
    "template_type": "text_based",
    "text_template": {"template_description":TEXT_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "text_based_slide": {
            "html_template": TEXT_BASED_HTML_TEMPLATE,
            "overlay_template": "",
            "text": {
                "headline": {"type": "text", "tag": "h1", "class": "headline"},
                "news_source": {"type": "text", "tag": "p", "class": "source"},
            },
            "assets":{
                "logo_image": {"type": "dropdown", "values": ["logo.png"], "default": "logo.png"},
                "background_image": {"type": "dropdown", "values": ["background.jpg"], "default": "background.jpg"},
            },
            ## No edits because background image not there
            "image_edits": {},
            "video_edits":{
                "type": {"type":"default", "values": "image_overlay"},
            }
        },
    },
}