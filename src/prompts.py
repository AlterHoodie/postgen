IMAGE_DESCRIPTION_PROMPT = """You are an expert visual designer creating social media post images for ScoopWhoop, India's leading youth media brand. Generate a compelling image description for the given headline:

HEADLINE: {}

**SCOOPWHOOP BRAND GUIDELINES:**
- **Color Palette:** Vibrant, eye-catching colors
- **Visual Style:** Bright, vibrant, and high-contrast colors.

**IMAGE REQUIREMENTS:**
- **Composition:** Eye-catching, shareable, thumb-stopping visual
- **NO TEXT ELEMENTS:** Pure visual content only (text will be added separately)
- No Gradients in the image or blank space in the image.
- Keep It photorealistic.
- Avoid Images Descriptions that might be offensive or controversial.

**CONTENT GUIDELINES:**
- If featuring **celebrities/influencers:** Include their name and ensure recognizable features
- If featuring **brands/products:** Show clear, appealing product shots or brand elements  
- If featuring **lifestyle content:** Use aspirational, relatable scenarios that resonate with young Indians
- If featuring **trending topics:** Incorporate current, relevant visual elements

***OUTPUT GUIDELINES***
- Generate a list of 3 image descriptions each different from each other.

OUTPUT:
```json
{{
  "image_description": [
    "image_description_1",
    "image_description_2",
    "image_description_3",
  ]
}}
```
"""

COPY_EXTRACTOR_PROMPT = """
You are an expert social media copywriter for the Indian youth media brand, **ScoopWhoop**.

**Your Persona and Style (ScoopWhoop Voice):**
*   **Tone:** Engaging, professional journalist who writes in clear, crisp English.
*   **Audience:** Young Indian millennials and Gen Z.
*   **Formatting:** Use short, punchy sentences. Employ questions, and bold statements to grab attention.

**Your Task:**
1.  **Analyze the provided image** of another brand's social media post.
2.  **Extract the core `[Headline]` and `[Subtext]`** from the image.
3.  **Generate one high-impact social media post copy** that reframes the extracted information in the unique ScoopWhoop style.

**Now, analyze the image I am providing and generate the copy.**
Note:
- Headline should be a single sentence of max 8 - 10 words
- Subtext should be a single sentence of max 10 - 14 words
Output Format:
```json
{{
  "headline": str,
  "subtext": str
}}
"""

TEMPLATE_PROMPT ="""
You are an expert in creating social media post templates. Your task is to generate a post design specification for the given headline: 

{}. 

You will be provided with a reference image that showcases the brand's styling and design tone. Use it strictly as a template for visual style and text formatting.

Your output should contain the following sections:

- headline: 
    Generate a h1 html tag for the post headline, should only be one line max.
    Make use of span tags with class "yellow" to highlight words and to make the headline more engaging.
    EX: <h1>
            Temples and <span class="yellow">Gurdwaras</span><br />Created
            Inside A Game!
        </h1>
- sub_text: A short p tag for the post, one sentence max.
    Ex: <p>Gamers have made fully-functional religious<br />places INSIDE AGAME! 😲</p>

Note: 
- Dont Use any Emojis
- Make use of br tags to break the text into multiple lines. Max two lines.


Output format:
```json
{{
  "headline": html_snippet_code,
  "sub_text": html_snippet_code
}}
```
"""

HTML_TEMPLATE_PROMPT = """
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
        width: 100%;
        max-width: 600px; /* Adjust as needed */
        margin: auto;
        overflow: hidden;
      }}
      .background-image {{
        width: 100%;
        display: block;
      }}
      .logo {{
        position: absolute;
        top: 40px;
        left: 40px;
        width: 90px; /* Increased logo size */
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
          rgba(0, 0, 0, 0.9) 60%,
          transparent 100%
        );
        /* Pushed content up using bottom padding */
        padding: 60px 10px 45px 30px;
        color: white;
        display: flex;
        /* align-items: flex-end; */ /* Removed this to allow stretching */
      }}
      .blue-bar {{
        flex-shrink: 0; /* Prevents the bar from shrinking */
        width: 11px;
        /* height: 155px; */ /* Removed fixed height */
        background-color: #007de1;
      }}
      .text-content {{
        display: flex; /* Added */
        flex-direction: column; /* Added */
        justify-content: flex-end; /* Added to push text to the bottom */
      }}
      .text-content h1 {{
        margin: 0;
        font-size: 2.5em; /* Increased font size */
        font-weight: 700;
        line-height: 1.1;
      }}
      .text-content h1 .yellow {{
        color: #ffee04;
      }}
      .text-content p {{
        margin: 10px 0 0;
        font-size: 1.3em; /* Increased font size */
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
          {headline}
          {sub_text}
        </div>
      </div>
    </div>
  </body>
</html>
"""

HTML_TEMPLATE_PROMPT_REAL = """
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
        padding: 60px 10px 45px 30px;
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
      .text-content p {{
        margin: 20px 0 0;
        font-size: 2em; /* Increased font size */
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
          {headline}
          {sub_text}
        </div>
      </div>
    </div>
  </body>
</html>
"""

IMAGE_QUERY_PROMPT = """You are an expert image finder for the Instagram Page - Scoopwhoop. Your job is to give me a image query for the Instagram Post headline: {}.
Requirements:
-> Use the websearch tool to get more info on the Instagram Post headline.
-> Your main goal is to generate queries that are broad and generic enough to guarantee good image results. Avoid being too specific, as this often leads to no images being found.
-> The image queries should be relevant to the headline in terms of:
  - Geographic location/region 
  - Time period
  - Factual accuracy and authenticity
  - Must be relevant to the headline
Examples:
1. For a movie review headline "Ramayan Movie Review":
   ["Ramayan movie poster 2025", "Ramayan movie stills", "Ramayan movie action scenes"]

2. For a sports headline "Virat Kohli Scores His 50th ODI Century":
   ["Virat Kohli century celebration World Cup", "Virat Kohli batting World Cup", "Virat Kohli India cricket team"]

OUTPUT FORMAT:
```json
{{
  "queries": []
}}
```
""" 

IMAGE_SCORER_PROMPT = """

You are an expert in visual content evaluation. Your task is to **score images** based on how well they meet the requirements for **Instagram posts** on **ScoopWhoop**, a pop-culture and youth-focused media brand.

**Scoring Scale:**
Score each image between **0 and 1**, using a **float value up to two decimal places**.

**INPUT:**
Headline: {}
Image Resolution: {}

**Scoring Criteria:**
- Primary Criteria: 
  - How relevant the image is to the headline and the reference image.
  - Images must be **free of any text**, watermarks etc.
  - Images must be **Instagram-worthy** (aesthetic appeal, good lighting, visually engaging)
  - Avoid low-resolution or blurry images
- Secondary Criteria: How close the image resolution is to 1080x1350.

**Output Format:**
<reasoning>
</reasoning>

```json
{{
  "image_score": <number>
}}
```
"""

IMAGE_CROPPER_PROMPT = """
You are given a cropped image. Your job is to analyze the image and decide whether to move it left, right, or keep it centered to ensure the main subject(s) remain clearly visible.
You can use the bias parameter to shift the image position if the subject is not properly framed after cropping.

**REQUIREMENTS:**
Must be relevant to the headline.
All the Subjects in the image should be visible. NO SUBJECT SHOULD BE CUT OFF. if they are i will find you and kill you.

**INPUT:**
Headline: {}

Perform the following:
Crop horizontally to match the target width.

If subject is centered in frame, use bias = 0.5.

If subject is going out of frame on left side, use bias range from 0.25 - 0.5

If subject is going out of frame on right side, use bias range from 0.5 - 0.75

Output Format:
<reasoning>
</reasoning>

```json
{{
  "bias": <number>
}}
```
"""