TEMPLATE_DESCRIPTION = """
Thumbnail: This Infomance template creates visually engaging thumbnail images featuring a main background image with three circular image overlays positioned in a unique layout. The design includes two circles in the left column and one circle in the right column, each highlighting different aspects of the story. The template combines bold text content with multiple visual elements to create compelling social media thumbnails.
The source should only be used if the post or the news is not from Infomance.
NOTE: Only one slide is required for this template.
"""

JSON_DESCRIPTION = """
This template has the following slides/sections:
Thumbnail Slide:
  ### Attributes:
  - This should be the opening slide of the storyboard. Must be eye catching and engaging.
    EX: A main background image of a political scene with three circular overlays showing different related images.
  
  - main_image_description: A one line description of the main background image.
    EX: "Prime Minister speaking at a podium with Indian flag in background"
  
  - circle_image_1_description: Description for the large circle (top-left position).
    EX: "Close-up of Vande Bharat train"
  
  - circle_image_2_description: Description for the medium circle (bottom-left position).  
    EX: "Group of people celebrating with flags"
  
  - circle_image_3_description: Description for the small circle (right position).
    EX: "Infrastructure development project site"
  
  - text_content: The main text content with highlighted portions using span class="highlight".
    EX: <span class="highlight">Street Dogs to be released</span> back to their localities, says supreme court
  
  - source: A p tag with classname-"source" for the source of the post.
    Ex: <p class="source">Source: TOI</p>

  ### Text Input:
    {{
      "name": "headline_slide",
      "main_image_description": "str",
      "circle_image_1_description": "str", 
      "circle_image_2_description": "str",
      "circle_image_3_description": "str",
      "text_template":{{
      "text_content": "<html_snippet_code>",
      "source": "<html_snippet_code>"
      }}
    }}

NOTE: 
- YOU CAN USE class name "highlight" to highlight key words in red color and make the content more engaging.
- DO NOT COMPLICATE THE IMAGE DESCRIPTIONS, KEEP IT SIMPLE AND DIRECT.
- DO NOT CITE SOURCES USING <a> tags. 
- Use Source tag to only cite external sources NOT INFOMANCE
- The three circle images should complement the main background image and provide additional visual context to the story.
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
        background-color: #dc1341;
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
        border-radius: 0 0 5px 5px;
        background-color: #dc1341;
        font-size: 50px;
        font-weight: 600;
        letter-spacing: 2px;
        padding: 1px 15px;
        margin: 0;
      }}

      .header {
        background-color: #ffffff;
        text-align: center;
        position: relative;
        display: flex;
        flex-direction: column;
        padding-bottom: 40px;
        border-bottom: 1px solid #ffffff;
      }}

      .headline {{
        text-align: center;
        padding: 15px 20px 25px 20px;
        background-color: #ffffff;
        font-family: "Poppins", sans-serif;
        font-weight: 800;
        font-size: 100px;
        color: #dc1341;
        margin: 0;
        line-height: 1.2;
      }}

      .image-banner {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0;
        overflow: hidden;
        position: relative;
      }}

      .main-image {{        
        width: 100%;
        height: auto;
        object-fit: contain;
        display: block;
      }}

      .circles-container {
        position: absolute;
        left: 60px;
        top: 60px;
        display: flex;
        gap: 20px;
        z-index: 10;
      }}

      .circle-column {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 30px;
      }}

      .circle-column.right {{
        justify-content: center;
        position: relative;
        top: 20px;
        right: 20px;
      }}

      .circle {{
        border-radius: 50%;
        border: 7px solid #dc1341;
        background-color: #ffffff;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        overflow: hidden;
      }}

      .circle.large {{
        width: 240px;
        height: 240px;
      }}
      .circle.medium {{
        width: 220px;
        height: 220px;
      }}
      .circle.small {{
        width: 210px;
        height: 210px;
      }}

      .circle img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
      }}

      .text-content {{
        padding: 40px 40px 60px 40px;
        background-color: #ffffff;
        text-align: center;
        font-family: "Poppins", sans-serif;
        font-weight: 700;
        font-size: 55px;
        color: #333;
        margin: 0;
        line-height: 1.4;
      }}

      .text-content .highlight {{
        color: #dc1341;
      }}

      .source {{
        font-family: "Poppins", sans-serif;
        font-size: 40px;
        font-weight: 800;
        color: #dc1341;
        margin-top: 20px;
        text-align: right;
      }}

      .footer-link {{
        font-family: "Poppins", sans-serif;
        font-weight: 300;
        font-size: 35px;
        background-color: #dc1341;
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

      <div class="image-banner">
        <img src="{main_image}" alt="Main Image" class="main-image" />
        <div class="circles-container">
          <div class="circle-column">
            <div class="circle large">
              <img src="{circle_image_1}" alt="Image 1" />
            </div>
            <div class="circle medium">
              <img src="{circle_image_2}" alt="Image 2" />
            </div>
          </div>
          <div class="circle-column right">
            <div class="circle small">
              <img src="{circle_image_3}" alt="Image 3" />
            </div>
          </div>
        </div>
      </div>

      <div class="text-content">
        {text_content}
      </div>

      {source}

      <div class="footer">
        <div class="footer-container">
          <div class="footer-link">www.infomance.com</div>
        </div>
      </div>
    </div>
  </body>
</html>
"""