TEMPLATE_DESCRIPTION = """This sarcastic indian template creates viral social media content by presenting bold, engaging narratives in a multi-slide format. It combines eye-catching headlines with detailed storytelling to deliver compelling content that resonates with audiences. The template uses a distinctive design to present stories, opinions, and narratives that spark conversation and engagement across social media platforms.
NOTE: 3-5 slides is the maximum number of slides you can have."""

JSON_DESCRIPTION = """
This template has the following slides/sections:
1. 1st Slide/Headline Slide:
  - This should be the opening slide of the storyboard. Must be eye catching and engaging.

  ### Attributes:
  - headline: The main headline of the story. Use **str** for highlighting important words and \\n for line breaks.
    EX: IPL just doesn't seem that **exciting** anymore.
  - news_source: Use source only to cite facts from other news sources and not to cite the_sarcastic_indian. Plain text only.
    Ex: Source: TOI
  ### Text Input:
    {{
      "name": "headline_slide",
      "text": {{
      "headline": "str",
      "news_source": "str"
      }}
    }}

2. Content Slide:
  These are content slides that provide additional context and details about the main headline. Each slide should:
  - Contain a **paragraph** of 3-4 concise lines of text that expand on a key aspect of the story
  - Maintain a clear narrative flow from the headline slide
  - Use engaging language while staying informative
  The goal is to tell a compelling story through text, without overwhelming the viewer with too much information at once.
  
  ### Attributes:
  - content: Use this to write content. Use **str** to highlight important sentences and \\n for line breaks.
    EX: **Rahul quit his dream job** after just 3 weeks.\\nHis parents were devastated, but he knew the toxic work culture was destroying his mental health.

  ### Text Input:
    {{
      "name": "content_slide",
      "text": {{
      "content": "str",
      }}
    }}

NOTE: 
- Use **str** to highlight parts of the text and \\n for new line.
- Use news_source tag to only cite external sources NOT the_sarcastic_indian.
"""

CONTENT_SLIDE_HTML_TEMPLATE = """
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
        font-size: 70px;
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
        {content}
    </div>
  </body>
</html>
"""


HEADLINE_SLIDE_HTML_TEMPLATE = """
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


writeup_template = {
    "page_name": "the_sarcastic_indian",
    "template_type": "writeup",
    "text_template": {"template_description":TEMPLATE_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "headline_slide": {
            "html_template": HEADLINE_SLIDE_HTML_TEMPLATE,
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
        "content_slide": {
            "html_template": CONTENT_SLIDE_HTML_TEMPLATE,
            "overlay_template": "",
            "text": {
                "content": {"type": "text", "tag": "h1", "class": "headline"},
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