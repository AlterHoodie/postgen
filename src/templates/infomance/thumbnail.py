TEMPLATE_DESCRIPTION = """
Infomance Thumbnail: This template creates professional news-style thumbnail images for social media posts. It features a black and red design scheme with the Infomance branding, combining a central image with bold headline text and source attribution. The layout is optimized for social media engagement with high contrast colors and clear typography.
The source should be used to cite external news sources when the content is not original to Infomance.
NOTE: Only one slide is required for this template.
"""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Infomance Thumbnail Slide:
  ### Attributes:
  - This should be the main slide for the news story. Must be professional and attention-grabbing.
    EX: A government building or official document image for policy announcements.
  
  - image_description: A one line description of the image you would like to use for the slide.
  - headline: The main headline displayed prominently at the top in red text.
    EX: "GOOD MOVE! 🇮🇳" Max three words
  
  - main_text: The primary news content text. Use **str** for highlighting important words and \\n for line breaks. Max one sentence.
    Ex: "Toll plaza will not charge **two wheelers & bikes** in India on National Highways!"
  
  - source: The source attribution for the news story.
    Ex: "- Government of India"

  ### Text Input:
    {{
      "name": "infomance_slide",
      "image_description": "str",
      "text": {{
      "headline": "str",
      "main_text": "str",
      "source": "str"
      }}
    }}

NOTE: 
- Use **str** to highlight important words. Use \n for line breaks if needed.
- DO NOT COMPLICATE THE IMAGE DESCRIPTIONS, KEEP IT SIMPLE AND DIRECT.
- Use Source to only cite external sources NOT INFOMANCE
- Keep headlines short and impactful for maximum engagement
"""

HEADLINE_SLIDE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Infomance</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");

      body,
      html {{
        margin: 0;
        padding: 0;
        font-family: sans-serif;
        display: flex;
        justify-content: center;
        min-height: 100vh;
        background-color: #000000;
      }}

      .container {{
        width: 1080px;
        background-color: #ffffff;
        height: 1350px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      .red-bar {{
        background-color: #d93a49;
        height: 25px;
        width: 100%;
        position: relative;
      }}
      .black-bar {{
        background-color: #000000;
        height: 50px;
        width: 100%;
        position: relative;
      }}

      .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0;
        overflow: hidden;
      }}
      .footer-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0;
        position: relative;
        top: -26px;
        z-index: 10;
      }}
      .logo {{
        font-family: "Times New Roman", Times, serif;
        color: #ffffff;
        background-color: #d93a49;
        font-size: 50px;
        font-weight: 600;
        letter-spacing: 2px;
        padding: 1px 15px;
        margin: 0;
      }}

      .header {{
        background-color: #ffffff;
        text-align: center;
        position: relative;
        display: flex;
        flex-direction: column;
        border-bottom: 1px solid #ffffff;
      }}

      .headline {{
        text-align: center;
        padding: 10px 20px 10px 20px;
        background-color: #ffffff;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 70px;
        color: #d93a49;
        margin: 0;
        line-height: 1.2;
      }}

      .image-banner {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0;
        overflow: hidden;
      }}

      .main-image {{
        width: 100%;
        height: auto;
        object-fit: cover;
        display: block;
      }}

      .text-content-container {{
        padding: 0px 20px 0px 20px;
        background-color: #ffffff;
        text-align: center;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 57px;
        color: #333;
        margin: 0;
        line-height: 1.3;
      }}

      .text-content {{
        padding: 30px 20px 40px 20px;
        background-color: #ffffff;
        text-align: center;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 57px;
        color: #333;
        margin: 0;
        line-height: 1.4;
      }}

      .text-content .yellow {{
        color: #d93a49;
      }}

      .yellow {{
        color: #d93a49;
      }}

      .source {{
        font-family: "Poppins", sans-serif;
        font-size: 40px;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 40px;
        text-align: right;
      }}
      .footer{{
        background-color: #000000;
      }}

      .footer-link {{
        font-family: "Poppins", sans-serif;
        font-weight: 300;
        font-size: 35px;
        background-color: #d93a49;
        padding: 0px 10px;
        letter-spacing: 1px;
        border-radius: 5px;
        text-align: center;
        color: white;
        text-decoration: none;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <div class="red-bar"></div>
        <div class="logo-container">
          <p class="logo">Infomance</p>
        </div>
      </div>

      <div class="headline">{headline}</div>

      <div class="image-banner">
        <img src="{background_image}" alt="Main Image" class="main-image" />
      </div>

      <div class="text-content-container">
        {main_text}
        {source}
      </div>

      <div class="footer">
        <div class="footer-container">
          <div class="footer-link">www.infomance.com</div>
        </div>
      </div>
    </div>
  </body>
</html>
"""


HEADLINE_SLIDE_OVERLAY_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Infomance</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");

      body,
      html {{
        margin: 0;
        padding: 0;
        font-family: sans-serif;
        display: flex;
        justify-content: center;
        min-height: 100vh;
        background-color: #000000;
      }}

      .container {{
        width: 1080px;
        background-color: #ffffff;
        height: 1350px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }}

      .red-bar {{
        background-color: #d93a49;
        height: 25px;
        width: 100%;
        position: relative;
      }}
      .black-bar {{
        background-color: #000000;
        height: 50px;
        width: 100%;
        position: relative;
      }}

      .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0;
        overflow: hidden;
      }}
      .footer-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0;
        position: relative;
        top: -26px;
        z-index: 10;
      }}
      .logo {{
        font-family: "Times New Roman", Times, serif;
        color: #ffffff;
        background-color: #d93a49;
        font-size: 50px;
        font-weight: 600;
        letter-spacing: 2px;
        padding: 1px 15px;
        margin: 0;
      }}

      .header {{
        background-color: #ffffff;
        text-align: center;
        position: relative;
        display: flex;
        flex-direction: column;
        border-bottom: 1px solid #ffffff;
      }}

      .headline {{
        text-align: center;
        padding: 10px 20px 10px 20px;
        background-color: #ffffff;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 70px;
        color: #d93a49;
        margin: 0;
        line-height: 1.2;
      }}

      .image-banner {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0;
        overflow: hidden;
      }}

      .main-video {{
        width: 100%;
        height: auto;
        object-fit: contain;
        display: block;
      }}  

      .text-content-container {{
        padding: 0px 20px 0px 20px;
        background-color: #ffffff;
        text-align: center;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 57px;
        color: #333;
        margin: 0;
        line-height: 1.3;
      }}

      .text-content {{
        padding: 30px 20px 40px 20px;
        background-color: #ffffff;
        text-align: center;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 57px;
        color: #333;
        margin: 0;
        line-height: 1.4;
      }}

      .text-content .yellow {{
        color: #d93a49;
      }}

      .yellow {{
        color: #d93a49;
      }}

      .source {{
        font-family: "Poppins", sans-serif;
        font-size: 40px;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 40px;
        text-align: right;
      }}

      .footer{{
        background-color: #000000;
      }}

      .footer-link {{
        font-family: "Poppins", sans-serif;
        font-weight: 300;
        font-size: 35px;
        background-color: #d93a49;
        padding: 0px 10px;
        letter-spacing: 1px;
        border-radius: 5px;
        text-align: center;
        color: white;
        text-decoration: none;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <div class="red-bar"></div>
        <div class="logo-container">
          <p class="logo">Infomance</p>
        </div>
      </div>

      <div class="headline">{headline}</div>

      <div class="image-banner">
        <video src="{background_video}" autoplay muted loop class="main-video"></video>
      </div>

      <div class="text-content-container">
        {main_text}
        {source}
      </div>

      <div class="footer">
        <div class="footer-container">
          <div class="footer-link">www.infomance.com</div>
        </div>
      </div>
    </div>
  </body>
</html>
"""

infomance_thumbnail_template = {
    "page_name": "infomance",
    "template_type": "thumbnail",
    "text_template": {"template_description":TEMPLATE_DESCRIPTION,
            "json_description":JSON_DESCRIPTION},
    "slides": {
        "infomance_slide": {
            "html_template": HEADLINE_SLIDE_HTML_TEMPLATE,
            "overlay_template": HEADLINE_SLIDE_OVERLAY_TEMPLATE,
            "text": {
                    "headline": {"type": "text_area", "tag": "h1", "class": "headline"},
                    "main_text": {"type": "text_area", "tag": "div", "class": "text-content"},
                    "source": {"type": "text", "tag": "p", "class": "source"},
            },
            "assets":{
                "background_video": {"type":"bytes", "file_type":"mp4"},
                "background_image": {"type":"bytes", "file_type":"png"},
            },
            "image_edits": {
            },
            "video_edits":{
                "type": {"type":"default", "values": "video_overlay"},
                "class_name":{"type":"default","values":"main-video"},
                "padding":{"type":"default","values":256},
            }
        },
    },
}