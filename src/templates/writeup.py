TEXT_TEMPLATE = """
Write Ups : This ScoopWhoop template uses a bold, eye-catching design to present engaging narratives in a snackable, multi-slide format for social media. It pairs strong imagery with large, highlighted text to quickly tell a story and is aimed at a young audience that consumes content on the go.

This template has the following slides/sections:
1. 1st Slide/Headline Slide:
  - This should be the opening slide of the storyboard. Must be eye catching and engaging.
    EX: A photo of a temple and a gurdwara created inside a game.
  - image_description: A one line description of the image you would like to use for the slide.
  - headline: The main headline of the story must be given as an html H1 tag 
    EX: <h1>
            Temples and <span class="yellow">Gurdwaras</span><br />Created
            Inside A Game!
        </h1>
  - subtext: A short p tag with classname-"subtext" for the post, one sentence max.
    Ex: <p class="subtext">Gamers have made fully-functional religious<br />places INSIDE AGAME! 😲</p>
  - is_trigger: Use when explicit/graphic visuals are required for the post.
    If required, use <p class='trigger-warning'>Trigger Warning</p> else fill "".
  Text Input:
    {{
      "name": "headline_slide",
      "image_description": "str",
      "text_template":{{
      "headline": "<html_snippet_code>",
      "subtext": "<html_snippet_code>",
      "is_trigger": "<html_snippet_code>"
      }}
    }}

2. Content Slide:
  These are content slides that are used to tell/expand the story behind the main headline. This slide should be text heavy.
  - image_description: A one line description of the image you would like to use for the slide.
    EX: A photo of a temple and a gurdwara created inside a game.
  - subtext: Use this tag to write content using p tags. should be 4-5 lines. use class yellow to highlight sentences.
    EX: <p class="subtext"><span class="yellow">A 'voter rights yatra' is planned from August17</span>, aiming to rally support and spotlight the claims.</p>

  Text Input:
    {{
      "name": "content_slide",
      "image_description": "str",
      "text_template":{{
      "subtext": "<html_snippet_code>",
      }}
    }}

NOTE: 
- YOU CAN USE class name "yellow" to highlight words and to make the headline more engaging. Use br tags to break the text into multiple lines.
- DO NOT COMPLICATE THE IMAGE DESCRIPTIONS, KEEP IT SIMPLE AND DIRECT.
- DO NOT CITE SOURCES USING <a> tags. 
- Use Source tag to only cite external sources NOT SCOOPWHOOP
- 3-4 slides is the maximum number of slides you can have.
"""


HEADLINE_SLIDE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title></title>
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
        top: 40px;
        left: 40px;
        width: 110px; /* Increased logo size */
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        bottom: 0; /* Anchored overlay to the bottom */
        left: 0;
        right: 0;
        /* Gradient from semi-transparent black to fully transparent */
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.95) 40%,
          rgba(0, 0, 0, 0.5) 75%,
          transparent 100%
        );
        /* Pushed content up using bottom padding */
        padding: 100px 10px 45px 30px;
        color: white;
        display: flex;
        /* align-items: flex-end; */ /* Removed this to allow stretching */
      }}
      .blue-bar {{
        flex-shrink: 0; /* Prevents the bar from shrinking */
        width: 18px;
        /* height: 155px; */ /* Removed fixed height */
        background-color: #007de1;
        margin-right: 20px;
        margin-left: 40px;
      }}
      .text-content {{
        display: flex; /* Added */
        flex-direction: column; /* Added */
        justify-content: flex-end; /* Added to push text to the bottom */
        /* margin: 0px 0 100px 0; */
      }}
      .text-content h1 {{
        margin: 0;
        font-size: 3.8em; /* Increased font size */
        font-weight: 700;
        line-height: 1.1;
      }}
      .text-content h1 .yellow {{
        color: #ffee04;
      }}
      .text-content .subtext {{
        margin: 5px 0 0;
        font-size: 2.5em; /* Increased font size */
      }}
      .text-content .subtext .yellow {{
        color: #ffee04;
      }}
      
      .text-content .source {{
        margin: 20px 0 0;
        font-size: 1.7em; /* Increased font size */
      }}
      .trigger-warning {{
        background-color: #a22513;
        color: white;
        padding: 4px 20px 9px;
        border-radius: 30px;
        font-size: 1.8em;
        font-weight: 700;
        width: fit-content;
        margin-top: 10px;
        margin-bottom: 15px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <img src="{file_path}" class="background-image" />
      <div class="text-overlay">
        <div class="blue-bar"></div>
        <div class="text-content">
          {is_trigger}
          {headline}
          {subtext}
        </div>
      </div>
    </div>
  </body>
</html>
"""

HEADLINE_SLIDE_OVERLAY_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title></title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Golos Text", sans-serif;
        background-color: #000000;
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
        top: 40px;
        left: 40px;
        width: 110px; /* Increased logo size */
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        bottom: 0; /* Anchored overlay to the bottom */
        left: 0;
        right: 0;
        /* Gradient from semi-transparent black to fully transparent */
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.95) 40%,
          rgba(0, 0, 0, 0.5) 75%,
          transparent 100%
        );
        /* Pushed content up using bottom padding */
        padding: 100px 10px 55px 30px;
        color: white;
        display: flex;
        /* align-items: flex-end; */ /* Removed this to allow stretching */
      }}
      .blue-bar {{
        flex-shrink: 0; /* Prevents the bar from shrinking */
        width: 18px;
        /* height: 155px; */ /* Removed fixed height */
        background-color: #007de1;
        margin-right: 20px;
        margin-left: 40px;
      }}
      .text-content {{
        display: flex; /* Added */
        flex-direction: column; /* Added */
        justify-content: flex-end; /* Added to push text to the bottom */
        /* margin: 0px 0 100px 0; */
      }}
      .text-content h1 {{
        margin: 0;
        font-size: 3.8em; /* Increased font size */
        font-weight: 700;
        line-height: 1.1;
      }}
      .text-content h1 .yellow {{
        color: #ffee04;
      }}
      .text-content .subtext {{
        margin: 5px 0 0;
        font-size: 2.5em; /* Increased font size */
      }}
      .text-content .subtext .yellow {{
        color: #ffee04;
      }}
      
      .text-content .source {{
        margin: 20px 0 0;
        font-size: 1.7em; /* Increased font size */
      }}
      .trigger-warning {{
        background-color: #a22513;
        color: white;
        padding: 4px 20px 9px;
        border-radius: 30px;
        font-size: 1.8em;
        font-weight: 700;
        width: fit-content;
        margin-top: 10px;
        margin-bottom: 15px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <div class="text-overlay">
        <div class="blue-bar"></div>
        <div class="text-content">
          {is_trigger}
          {headline}
          {subtext}
        </div>
      </div>
    </div>
  </body>
</html>
"""

CONTENT_SLIDE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title></title>
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
        top: 40px;
        left: 40px;
        width: 110px; /* Increased logo size */
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        bottom: 0; /* Anchored overlay to the bottom */
        left: 0;
        right: 0;
        /* Gradient from semi-transparent black to fully transparent */
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.95) 40%,
          rgba(0, 0, 0, 0.5) 75%,
          transparent 100%
        );
        /* Pushed content up using bottom padding */
        padding: 100px 10px 45px 30px;
        color: white;
        display: flex;
        /* align-items: flex-end; */ /* Removed this to allow stretching */
      }}
      .blue-bar {{
        flex-shrink: 0; /* Prevents the bar from shrinking */
        width: 18px;
        /* height: 155px; */ /* Removed fixed height */
        background-color: #007de1;
        margin-right: 20px;
        margin-left: 40px;
      }}
      .text-content {{
        display: flex; /* Added */
        flex-direction: column; /* Added */
        justify-content: flex-end; /* Added to push text to the bottom */
        /* margin: 0px 0 100px 0; */
      }}
      .text-content h1 {{
        margin: 0;
        font-size: 3.8em; /* Increased font size */
        font-weight: 700;
        line-height: 1.1;
      }}
      .text-content h1 .yellow {{
        color: #ffee04;
      }}
      .text-content .subtext {{
        margin: 5px 0 0;
        font-size: 2.5em; /* Increased font size */
      }}
      .text-content .subtext .yellow {{
        color: #ffee04;
      }}
      
      .text-content .source {{
        margin: 20px 0 0;
        font-size: 1.7em; /* Increased font size */
      }}
      .trigger-warning {{
        background-color: #a22513;
        color: white;
        padding: 4px 20px 9px;
        border-radius: 30px;
        font-size: 1.8em;
        font-weight: 700;
        width: fit-content;
        margin-top: 10px;
        margin-bottom: 15px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <img src="{file_path}" class="background-image" />
      <div class="text-overlay">
        <div class="blue-bar"></div>
        <div class="text-content">
          {subtext}
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
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Golos Text", sans-serif;
        background-color: #000000;
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
        top: 40px;
        left: 40px;
        width: 110px; /* Increased logo size */
        filter: brightness(0) invert(1);
      }}
      .text-overlay {{
        position: absolute;
        bottom: 0; /* Anchored overlay to the bottom */
        left: 0;
        right: 0;
        /* Gradient from semi-transparent black to fully transparent */
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.95) 40%,
          rgba(0, 0, 0, 0.5) 75%,
          transparent 100%
        );
        /* Pushed content up using bottom padding */
        padding: 100px 10px 55px 30px;
        color: white;
        display: flex;
        /* align-items: flex-end; */ /* Removed this to allow stretching */
      }}
      .blue-bar {{
        flex-shrink: 0; /* Prevents the bar from shrinking */
        width: 18px;
        /* height: 155px; */ /* Removed fixed height */
        background-color: #007de1;
        margin-right: 20px;
        margin-left: 40px;
      }}
      .text-content {{
        display: flex; /* Added */
        flex-direction: column; /* Added */
        justify-content: flex-end; /* Added to push text to the bottom */
        /* margin: 0px 0 100px 0; */
      }}
      .text-content h1 {{
        margin: 0;
        font-size: 3.8em; /* Increased font size */
        font-weight: 700;
        line-height: 1.1;
      }}
      .text-content h1 .yellow {{
        color: #ffee04;
      }}
      .text-content .subtext {{
        margin: 5px 0 0;
        font-size: 2.5em; /* Increased font size */
      }}
      .text-content .subtext .yellow {{
        color: #ffee04;
      }}
      
      .text-content .source {{
        margin: 20px 0 0;
        font-size: 1.7em; /* Increased font size */
      }}
      .trigger-warning {{
        background-color: #a22513;
        color: white;
        padding: 4px 20px 9px;
        border-radius: 30px;
        font-size: 1.8em;
        font-weight: 700;
        width: fit-content;
        margin-top: 10px;
        margin-bottom: 15px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <div class="text-overlay">
        <div class="blue-bar"></div>
        <div class="text-content">
          {subtext}
        </div>
      </div>
    </div>
  </body>
</html>
"""

writeup_template = {
    "template_type": "writeup",
    "text_template": TEXT_TEMPLATE,
    "slides": {
        "headline_slide": {"html_template": HEADLINE_SLIDE_HTML_TEMPLATE, 
                           "overlay_template": HEADLINE_SLIDE_OVERLAY_TEMPLATE,
                           "text_json":{
                                "name": "headline_slide",
                                "image_description": "str",
                                "text_template":{
                                "headline": {"type":"text","tag":"h1","class":""},
                                "subtext": {"type":"text","tag":"p","class":"subtext"},
                                "is_trigger": {"type":"checkbox","html_snippet":"<p class='trigger-warning'>Trigger Warning</p>"}
                                }
                           }},
        "content_slide": {"html_template": CONTENT_SLIDE_HTML_TEMPLATE, 
                           "overlay_template": CONTENT_SLIDE_OVERLAY_TEMPLATE,
                           "text_json":{
                                "name": "content_slide",
                                "image_description": "str",
                                "text_template":{
                                "subtext": {"type":"text_area","tag":"p","class":"subtext"},
                                }
                           }},
    }
}