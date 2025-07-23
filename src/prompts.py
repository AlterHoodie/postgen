INPUT_TEMPLATE_PROMPT = """
Review the Generated Background Image and headline and generate the following JSON Output Template. 
Headline:
{}

JSON INPUT TEMPLATE:
{}

- TIPS TO CHOOSE COLORS : background color for highlighted text spans. Choose a contrasting color that maintains readability against both the background color and image background.
- Generate Catchy Sentence and make use of highlights(if possible) to make the post more visually appealing and engaging. 
- The Sentences should fit inside the Instagram post.
JSON OUTPUT TEMPLATE:
```json
{{}}
```
"""

HTML_TEMPLATE_PROMPT = """
You are a senior HTML developer tasked with creating a General Reusable HTML template for social media posts. Your goal is to replicate the design and typography exactly as shown in the reference image provided.

Instructions:

HTML Structure:
Post Topic: {}
Create the html template for the given post topic, 

Create a single, standalone Python Formatable html string with no external CSS or JavaScript.
Must be Python Formatable string, so use "{{{{}}}}" for normal-css-syntax curly braces and "{{<variable_name>}}" for input variables. 

Variables To include:
 - background_image_url : for the inserting background image url
 - logo_url : for inserting logo url

Variables to Generate:
 - Generate simple variables for headline, subtext , highlight text, font_color, highlight_font color etc. Keep it simple and short and dont create too many variables.


Structure the content using only <div> elements.

Text should be placed exactly as shown in the image.

-> Typography and Design:

	* Replicate the exact fonts, font sizes, line heights, colors, and letter spacing from the image.
	* Match the highlighted headline style, including background color, padding, positioning, and box styling.
  * Use Placeholder text and image src links in template
	* The background or image area should be defined using an <img> tag 
	* Use placeholder variables for image src links. For the background image use resolution 1024x1536.

-> CSS Styling:

	* Use a <style> tag in the <head> of the HTML file for all CSS.
	* Do not use JavaScript.
	* Use Flexbox or absolute positioning based on which better matches the visual layout from the image.
	* No need to import social media icons, or arrows—they are assumed to be part of the image and will be handled separately.

-> No External Dependencies:
	* Do not use external icons, or libraries.
	* The file must be fully self-contained and portable.
  * No Emojis or watermarks

Output:
A Python Formatable html string along with its json input template.

```html
HTML_STRING
```
"""

IMAGE_DESCRIPTION_PROMPT = """You are an expert visual designer creating social media post images for ScoopWhoop, India's leading youth media brand. Generate a compelling image description for the given headline:

HEADLINE: {}

**SCOOPWHOOP BRAND GUIDELINES:**
- **Color Palette:** Vibrant, eye-catching colors
- **Visual Style:** Bright, vibrant, and high-contrast colors.

**IMAGE REQUIREMENTS:**
- **Composition:** Eye-catching, shareable, thumb-stopping visual
- **NO TEXT ELEMENTS:** Pure visual content only (text will be added separately)

**CONTENT GUIDELINES:**
- If featuring **celebrities/influencers:** Include their name and ensure recognizable features
- If featuring **brands/products:** Show clear, appealing product shots or brand elements  
- If featuring **lifestyle content:** Use aspirational, relatable scenarios that resonate with young Indians
- If featuring **trending topics:** Incorporate current, relevant visual elements

Generate a detailed, specific image description that an AI image generator can execute perfectly.

Output Format:
```json
{{
  "image_description": str
}}
```
"""

IMAGE_DESCRIPTION_WITH_TEXT_PROMPT = """You are an expert visual designer creating social media post images with integrated text for ScoopWhoop, India's leading youth media brand. Generate a compelling image description that includes text elements for the given headline:

HEADLINE: {}

**SCOOPWHOOP BRAND GUIDELINES:**
- **Color Palette:** Vibrant, eye-catching colors
- **Typography Style:** Bold, modern, highly readable fonts with strong contrast

**IMAGE WITH TEXT REQUIREMENTS:**
- **Text Placement:** Bottom third of the image, ensuring readability
- **Reference Image:** Use the reference image for textual design, placement and colors.

**CONTENT GUIDELINES:**
- If featuring **celebrities/influencers:** Include their name in text and ensure recognizable features
- If featuring **brands/products:** Include brand name/product name in the text elements
- If featuring **lifestyle content:** Use relatable text that connects with young Indian audience
- If featuring **trending topics:** Include relevant hashtags or trending phrases in the design
- No Hashtags or Emojis

Generate a detailed, specific image description that includes both visual elements and text integration for an AI image generator.

Output Format:
```json
{{
  "image_description": str
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