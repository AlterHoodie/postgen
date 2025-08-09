TEXT_TEMPLATE = """
**Template Name:** TimeLine

**Primary Goal:** To generate content for a multi-slide visual storyboard that presents chronological stories, updates, or milestones. The output must follow a strict JSON format for each slide, detailing text and image descriptions.

**General Instructions:**
*   Adhere strictly to the specified HTML tags and class names in the examples.
*   Pay close attention to the word and line count limits for each field.
*   Image descriptions should be concise yet evocative, suitable for an AI image generator.
*   Ensure all text is proofread and fits the narrative context of a timeline.

---

### Slide / Section Definitions

**1. Headline Slide**
*   **Purpose:** The opening slide of the storyboard. It must be eye-catching and create a strong first impression of the story.
*   **`image_description`:** A clear, one-line description of the desired background image. Focus on the mood, subject, and style. (e.g., "A dramatic, wide-angle shot of a crowded city street at night").
*   **`first_line`:** The main headline of the story. Must be a powerful statement of **no more than 3-4 words**.
    *   **Format:** `<div class="first-line">YOUR HEADLINE HERE</div>`
*   **`highlight`:** The highlighted keyword or phrase of the headline. Must be **no more than 3-4 words**.
    *   **Format:** `<div class="highlight">HIGHLIGHTED TEXT HERE</div>`
*   **`sub_heading`:** A concise subheading that provides additional context to the headline. **Must not exceed one line or 8-10 words.**
    *   **Format:** `<div class="sub-heading">Your sub-heading here</div>`

*   **Text Input Structure:**
    {
      "name": "headline_slide",
      "image_description": "str",
      "text_template": {
        "first_line": "<html_snippet_code>",
        "highlight": "<html_snippet_code>",
        "sub_heading": "<html_snippet_code>"
      }
    }

**2. Timeline Start Slide**
*   **Purpose:** This slide marks the first event or the beginning of the chronological sequence.
*   **`image_description`:** A one-line description of an image relevant to this specific event in the timeline.
*   **`timeline_highlight`:** The timestamp for the event. **Must be in a "Time, Date" format** (e.g., `10:30 PM, 9TH JUNE`). This field should only contain the time and date.
    *   **Format:** `<div class="timeline-highlight">10:30 PM, 9TH JUNE</div>`
*   **`body_text`:** The main descriptive text for this event. Expand on the story in **4-5 lines**, explaining what happened at this point in time.
    *   **Format:** `<p class="body-text">Your full body text goes here...</p>`

*   **Text Input Structure:**
    {
      "name": "timeline_start_slide",
      "image_description": "str",
      "text_template": {
        "timeline_highlight": "<html_snippet_code>",
        "body_text": "<html_snippet_code>"
      }
    }

**3. Timeline Middle Slide**
*   **Purpose:** This slide is for any subsequent event between the start and the end of the timeline. Use it for all intermediate milestones.
*   **`image_description`:** A one-line description of an image relevant to this specific event in the timeline.
*   **`timeline_highlight`:** The timestamp for the event. **Must be in a "Time, Date" format** (e.g., `11:00 PM, 9TH JUNE`). This field should only contain the time and date.
    *   **Format:** `<div class="timeline-highlight">11:00 PM, 9TH JUNE</div>`
*   **`body_text`:** The main descriptive text for this event. Expand on the story in **4-5 lines**, explaining what happened at this point in time.
    *   **Format:** `<p class="body-text">Your full body text goes here...</p>`

*   **Text Input Structure:**
    {
      "name": "timeline_middle_slide",
      "image_description": "str",
      "text_template": {
        "timeline_highlight": "<html_snippet_code>",
        "body_text": "<html_snippet_code>"
      }
    }

**4. Timeline End Slide**
*   **Purpose:** This is the concluding event of the timeline, used to wrap up the story or present the final milestone.
*   **`image_description`:** A one-line description of an image relevant to this final event in the timeline.
*   **`timeline_highlight`:** The timestamp for the final event. **Must be in a "Time, Date" format** (e.g., `1:30 AM, 10TH JUNE`). This field should only contain the time and date.
    *   **Format:** `<div class="timeline-highlight">1:30 AM, 10TH JUNE</div>`
*   **`body_text`:** The main descriptive text for this final event. Expand on the story's conclusion in **4-5 lines**.
    *   **Format:** `<p class="body-text">Your full body text goes here...</p>`

*   **Text Input Structure:**
    {
      "name": "timeline_end_slide",
      "image_description": "str",
      "text_template": {
        "timeline_highlight": "<html_snippet_code>",
        "body_text": "<html_snippet_code>"
      }
    }

NOTE:
- 3-4 slides is the maximum number of slides you can have.
"""

HEADLINE_SLIDE_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Template</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@700&display=swap");
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Bebas Neue", sans-serif;
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
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 1) 30%,
          rgba(0, 0, 0, 0) 100%
        );
        padding: 60px 40px 70px 40px;
        color: white;
        text-align: center;
      }}

      .first-line {{
        font-size: 110px;
        font-weight: 590;
        line-height: 1.2;
        display: inline-block;
        transform: scaleY(1.1);
      }}

      .highlight {{
        background-color: #fbe10a;
        color: black;
        padding: 5px 20px 0px 20px;
        font-size: 110px;
        display: inline-block;
        /* margin-top: 2px; Closer to the first line */
        font-weight: 590;
        line-height: 1.2;
        transform: scaleY(1.1);
      }}

      .dashed-line {{
        width: 780px;
        height: 3px; /* thickness of line */
        margin: 28px auto 20px auto;
        background-image: repeating-linear-gradient(
          to right,
          white 0 3px,
          /* dash length */ transparent 10px 15px /* gap length */
        );
      }}

      .sub-heading {{
        background-color: white;
        color: black;
        font-family: "Golos Text", sans-serif;
        font-weight: 700;
        font-size: 32px;
        padding: 8px 40px;
        display: inline-block;
        border-radius: 3px;
        letter-spacing: 0px;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <img src="{file_path}" class="background-image" />
      <div class="text-overlay">
        {first_line}
        {highlight}
        <div class="dashed-line"></div>
        {sub_heading}
      </div>
      </div>
    </div>
  </body>
</html>
"""

TIMELINE_START_SLIDE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Template - Modular Timeline</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@700&display=swap");
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Bebas Neue", sans-serif;
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
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.9) 10%,
          rgba(0, 0, 0, 0.9) 40%,
          rgba(0, 0, 0, 0.8) 50%,
          rgba(0, 0, 0, 0.5) 70%,
          rgba(0, 0, 0, 0) 100%
        );
        padding: 70px 80px 20px 80px;
        color: white;
        text-align: center;
      }}

      /* --- MODULAR TIMELINE STYLES START --- */

      /* This is the flex container for the line-circle-line structure */
      .timeline-track {{
        display: flex;
        align-items: center;
        /* Use negative margin to break out of the parent's padding */
        margin: 0 -80px;
        margin-bottom: 50px; /* Creates space for the connector to connect */
      }}

      /* Style for the horizontal line elements */
      .line {{
        height: 3px;
        background-color: #fbe10a;
        flex-grow: 1; /* This makes the lines fill the available space */
      }}
      .no_line {{
        height: 3px;
        background-color: transparent;
        flex-grow: 1; /* This makes the lines fill the available space */
      }}

      /* Style for the circle element */
      .circle {{
        width: 25px;
        height: 25px;
        background-color: #fbe10a;
        border-radius: 50%;
        flex-shrink: 0; /* Prevents the circle from shrinking */
        position: relative;
      }}

      /* The vertical line connecting the circle down to the highlight box */
      .circle::after {{
        content: "";
        position: absolute;
        left: 50%;
        top: 100%;
        transform: translateX(-50%);
        width: 3px;
        height: 50px; /* Length of the connector line */
        background-color: #fbe10a;
      }}

      /* --- MODULAR TIMELINE STYLES END --- */

      .timeline-highlight {{
        background-color: #fbe10a;
        color: black;
        padding: 5px 20px 0px 20px;
        font-size: 95px;
        display: inline-block;
        /* margin-top: 2px; Closer to the first line */
        font-weight: 590;
        letter-spacing: 2px;
        /* line-height: 1.1; */
        transform: scaleY(1.1);
      }}

      .body-text {{
        font-family: "Golos Text", sans-serif;
        font-weight: 400;
        font-size: 38px;
        line-height: 1.4;
        text-align: center;
        margin-top: 40px;
        color: #ffffff;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <img src="{file_path}" class="background-image" />
      <div class="text-overlay">
        <!-- MODIFIED TIMELINE STRUCTURE -->
        <div class="timeline-track">
          <div class="no_line"></div>
          <div class="circle"></div>
          <div class="line"></div>
        </div>
        {timeline_highlight}
        {body_text}
      </div>
    </div>
  </body>
</html>
"""

TIMELINE_MIDDLE_SLIDE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Template - Modular Timeline</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@700&display=swap");
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Bebas Neue", sans-serif;
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
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.9) 10%,
          rgba(0, 0, 0, 0.9) 40%,
          rgba(0, 0, 0, 0.8) 50%,
          rgba(0, 0, 0, 0.5) 70%,
          rgba(0, 0, 0, 0) 100%
        );
        padding: 70px 80px 20px 80px;
        color: white;
        text-align: center;
      }}

      /* --- MODULAR TIMELINE STYLES START --- */

      /* This is the flex container for the line-circle-line structure */
      .timeline-track {{
        display: flex;
        align-items: center;
        /* Use negative margin to break out of the parent's padding */
        margin: 0 -80px;
        margin-bottom: 50px; /* Creates space for the connector to connect */
      }}

      /* Style for the horizontal line elements */
      .line {{
        height: 3px;
        background-color: #fbe10a;
        flex-grow: 1; /* This makes the lines fill the available space */
      }}
      .no_line {{
        height: 3px;
        background-color: transparent;
        flex-grow: 1; /* This makes the lines fill the available space */
      }}

      /* Style for the circle element */
      .circle {{
        width: 25px;
        height: 25px;
        background-color: #fbe10a;
        border-radius: 50%;
        flex-shrink: 0; /* Prevents the circle from shrinking */
        position: relative;
      }}

      /* The vertical line connecting the circle down to the highlight box */
      .circle::after {{
        content: "";
        position: absolute;
        left: 50%;
        top: 100%;
        transform: translateX(-50%);
        width: 3px;
        height: 50px; /* Length of the connector line */
        background-color: #fbe10a;
      }}

      /* --- MODULAR TIMELINE STYLES END --- */

      .timeline-highlight {{
        background-color: #fbe10a;
        color: black;
        padding: 5px 20px 0px 20px;
        font-size: 95px;
        display: inline-block;
        /* margin-top: 2px; Closer to the first line */
        font-weight: 590;
        letter-spacing: 2px;
        /* line-height: 1.1; */
        transform: scaleY(1.1);
      }}

      .body-text {{
        font-family: "Golos Text", sans-serif;
        font-weight: 400;
        font-size: 38px;
        line-height: 1.4;
        text-align: center;
        margin-top: 40px;
        color: #ffffff;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <img src="{file_path}" class="background-image" />
      <div class="text-overlay">
        <!-- MODIFIED TIMELINE STRUCTURE -->
        <div class="timeline-track">
          <div class="line"></div>
          <div class="circle"></div>
          <div class="line"></div>
        </div>
        {timeline_highlight}
        {body_text}
      </div>
    </div>
  </body>
</html>
"""

TIMELINE_END_SLIDE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SW Template - Modular Timeline</title>
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@700&display=swap");
      @import url("https://fonts.googleapis.com/css2?family=Golos+Text:wght@400..900&display=swap");
      body,
      html {{
        margin: 0;
        padding: 0;
        height: 100%;
        font-family: "Bebas Neue", sans-serif;
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
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.9) 10%,
          rgba(0, 0, 0, 0.9) 40%,
          rgba(0, 0, 0, 0.8) 50%,
          rgba(0, 0, 0, 0.5) 70%,
          rgba(0, 0, 0, 0) 100%
        );
        padding: 70px 80px 20px 80px;
        color: white;
        text-align: center;
      }}

      /* --- MODULAR TIMELINE STYLES START --- */

      /* This is the flex container for the line-circle-line structure */
      .timeline-track {{
        display: flex;
        align-items: center;
        /* Use negative margin to break out of the parent's padding */
        margin: 0 -80px;
        margin-bottom: 50px; /* Creates space for the connector to connect */
      }}

      /* Style for the horizontal line elements */
      .line {{
        height: 3px;
        background-color: #fbe10a;
        flex-grow: 1; /* This makes the lines fill the available space */
      }}
      .no_line {{
        height: 3px;
        background-color: transparent;
        flex-grow: 1; /* This makes the lines fill the available space */
      }}

      /* Style for the circle element */
      .circle {{
        width: 25px;
        height: 25px;
        background-color: #fbe10a;
        border-radius: 50%;
        flex-shrink: 0; /* Prevents the circle from shrinking */
        position: relative;
      }}

      /* The vertical line connecting the circle down to the highlight box */
      .circle::after {{
        content: "";
        position: absolute;
        left: 50%;
        top: 100%;
        transform: translateX(-50%);
        width: 3px;
        height: 50px; /* Length of the connector line */
        background-color: #fbe10a;
      }}

      /* --- MODULAR TIMELINE STYLES END --- */

      .timeline-highlight {{
        background-color: #fbe10a;
        color: black;
        padding: 5px 20px 0px 20px;
        font-size: 95px;
        display: inline-block;
        /* margin-top: 2px; Closer to the first line */
        font-weight: 590;
        letter-spacing: 2px;
        /* line-height: 1.1; */
        transform: scaleY(1.1);
      }}

      .body-text {{
        font-family: "Golos Text", sans-serif;
        font-weight: 400;
        font-size: 38px;
        line-height: 1.4;
        text-align: center;
        margin-top: 40px;
        color: #ffffff;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <img src="./logo.png" alt="SW Logo" class="logo" />
      <img src="{file_path}" class="background-image" />
      <div class="text-overlay">
        <!-- MODIFIED TIMELINE STRUCTURE -->
        <div class="timeline-track">
          <div class="line"></div>
          <div class="circle"></div>
          <div class="no_line"></div>
        </div>
        {timeline_highlight}
        {body_text}
      </div>
    </div>
  </body>
</html>
"""

timeline_template = {
    "template_type": "timeline",
    "text_template": TEXT_TEMPLATE,
    "slides": {
        "headline_slide": {"html_template": HEADLINE_SLIDE_HTML_TEMPLATE, 
                           "overlay_template": "",
                           "text_json":{
                                "name": "headline_slide",
                                "image_description": "str",
                                "text_template":{
                                "first_line": {"type":"text","tag":"div","class":"first-line"},
                                "highlight": {"type":"text","tag":"div","class":"highlight"},
                                "sub_heading": {"type":"text","tag":"div","class":"sub-heading"}
                                }
                           }},
        "timeline_start_slide": {"html_template": TIMELINE_START_SLIDE_TEMPLATE, 
                                 "overlay_template": "",
                                 "text_json":{
                                    "name": "timeline_start_slide",
                                    "image_description": "str",
                                    "text_template":{
                                        "timeline_highlight": {"type":"text","tag":"div","class":"timeline-highlight"},
                                        "body_text": {"type":"text","tag":"p","class":"body-text"}
                                    }
                                }},
        "timeline_middle_slide": {"html_template": TIMELINE_MIDDLE_SLIDE_TEMPLATE, 
                                 "overlay_template": "",
                                 "text_json":{
                                    "name": "timeline_middle_slide",
                                    "image_description": "str",
                                    "text_template":{
                                        "timeline_highlight": {"type":"text","tag":"div","class":"timeline-highlight"},
                                        "body_text": {"type":"text","tag":"p","class":"body-text"}
                                    }
                                }},
        "timeline_end_slide": {"html_template": TIMELINE_END_SLIDE_TEMPLATE, 
                                 "overlay_template": "",
                                 "text_json":{
                                    "name": "timeline_end_slide",
                                    "image_description": "str",
                                    "text_template":{
                                        "timeline_highlight": {"type":"text","tag":"div","class":"timeline-highlight"},
                                        "body_text": {"type":"text","tag":"p","class":"body-text"}
                                    }
                                }},
        }
}

if __name__ == "__main__":
    text = {
            "name": "headline_slide",
            "image_description": "Wreckage of Air India Flight 171 at crash site",
            "text_template": {
                "first_line": "<div class=\"first-line\">Air India Flight 171 Tragedy</div>",
                "highlight": "<div class=\"highlight\">Catastrophic Crash After Takeoff</div>",
                "sub_heading": "<div class=\"sub-heading\">A Timeline of the Fateful Events</div>"
            }
        }

    with open("./data_/bleh_4.html", "w") as f:
        f.write(HEADLINE_SLIDE_HTML_TEMPLATE.format(file_path="./test.png", **text['text_template']))