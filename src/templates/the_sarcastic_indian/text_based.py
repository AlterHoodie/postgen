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
    EX: <h1>
            IPL just doesn't seem that
            <span class="yellow">exciting</span> anymore.
        </h1>
  - subtext: A short p tag with classname-"subtext" for the post, one sentence max.
    Ex: <p class="subtext">And then I realized mummy <br/> hamesha last mai kyun khaati thi.</p>
  ### Text Input:
    {{
      "name": "text_based_slide",
      "text_template":{{
      "headline": "<html_snippet_code>",
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
      html {
        margin: 0;
        padding: 0;
        font-family: "Inter", sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #f0f0f0;
      }

      .post-container {
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
      }

      .logo {
        position: absolute;
        top: -40px;
        left: 10px;
        width: 270px;
      }

      .headline {
        font-size: 90px;
        font-weight: 700;
        line-height: 1.3;
        text-align: left;
        width: 100%;
      }

      .swipe {
        position: absolute;
        bottom: 0px;
        right: 55px;
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 20px;
      }

      .source {
        position: absolute;
        bottom: 0px;
        left: 20px;
        font-size: 25px;
        font-style: italic;
        font-weight: 500; /* Regular weight */
        margin-bottom: 20px;
      }
    </style>
  </head>
  <body>
    <div class="post-container">
      <h1 class="headline">
        {headline}
      </h1>
      <p class="source">{news_source}</p>
      <p class="swipe">Swipe>>></p>
    </div>
  </body>
</html>

"""