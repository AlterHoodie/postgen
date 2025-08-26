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
    EX: "GOOD MOVE! 🇮🇳"
  
  - main_text: The primary news content text with optional highlighting.
    Ex: "Toll plaza will not charge <span class=\"highlight\">two wheelers & bikes</span> in India on National Highways!"
  
  - source: The source attribution for the news story.
    Ex: "- Government of India"

  ### Text Input:
    {{
      "name": "infomance_slide",
      "image_description": "str",
      "text_template":{{
      "headline": "str",
      "main_text": "str_with_highlight_spans",
      "source": "str"
      }}
    }}

NOTE: 
- YOU CAN USE class name "highlight" to highlight important words in red. Use <br/> tags to break text into multiple lines if needed.
- DO NOT COMPLICATE THE IMAGE DESCRIPTIONS, KEEP IT SIMPLE AND DIRECT.
- DO NOT CITE SOURCES USING <a> tags. 
- Use Source tag to only cite external sources NOT INFOMANCE
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
        background-color: #000000;
        height: 1350px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: center;
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
        padding: 15px 20px 25px 20px;
        background-color: #ffffff;
        font-family: "Poppins", sans-serif;
        font-weight: 800;
        font-size: 100px;
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
        object-fit: contain;
        display: block;
      }}

      .text-content {{
        padding: 30px 40px;
        background-color: #ffffff;
        text-align: center;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 65px;
        color: #333;
        margin: 0;
        line-height: 1.4;
      }}

      .text-content .highlight {{
        color: #d93a49;
      }}

      .source {{
        font-family: "Poppins", sans-serif;
        font-size: 40px;
        font-weight: 800;
        color: #d93a49;
        margin-top: 20px;
        text-align: right;
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
        <img src="{image_url}" alt="Main Image" class="main-image" />
      </div>

      <div class="text-content">
        {main_text}
        <p class="source">{source}</p>
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