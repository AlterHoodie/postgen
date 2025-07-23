IMAGE_DESCRIPTION_PROMPT = """You are an expert visual designer creating social media post images for ScoopWhoop, India's leading youth media brand. Generate a compelling image description for the given headline:

HEADLINE: {}

**SCOOPWHOOP BRAND GUIDELINES:**
- **Color Palette:** Vibrant, eye-catching colors
- **Visual Style:** Bright, vibrant, and high-contrast colors.

**IMAGE REQUIREMENTS:**
- **Composition:** Eye-catching, shareable, thumb-stopping visual
- **NO TEXT ELEMENTS:** Pure visual content only (text will be added separately)
- Leave space for text to be added in the bottom of the image.
- No Gradients in the image or blank space in the image.
- Keep It photorealistic.

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
*   **Tone:** Witty, relatable, conversational, and slightly informal. Use a mix of English and Hindi (Hinglish).
*   **Audience:** Young Indian millennials and Gen Z. The content should resonate with their everyday experiences, pop culture interests, and sense of humor.
*   **Formatting:** Use short, punchy sentences. Employ lists, questions, and bold statements to grab attention. Emojis are a must to add personality.

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
        margin-right: 15px;
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