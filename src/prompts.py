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

IMAGE_QUERY_PROMPT = """**You are a Head Photo Editor for the Instagram Page - ScoopWhoop.** Your role is to generate precise Google image search queries to find the most appropriate photo for a news headline.

Your most important task is to first analyze the headline and decide on the correct image strategy.
Today's date: 2025-08-04
**Headline:** {}

---

### **Core Principles for Query Generation:**

**1. The "Broad to Specific" Funnel:**
- Start with a broad, high-level query that captures the main subject.
- Create more specific variations by adding context like the event, location, or year. This gives you the best chance of finding a usable image. EX: Use location India as a keyword if the headline is about an Indian event/movie/ott series.

**2. Think in Image Categories (Query Diversity):**
Do not just search for the subject. Generate queries for different *types* of shots. Your queries should aim to find:
- **Hero/Portrait Shots:** Tightly cropped, high-quality photos of the main person involved. Often good for celebrity or human-interest stories.
  - *Example: "Liam Neeson portrait 2025", "Zendaya red carpet Met Gala"*
- **Action/Event Shots:** Images that capture a key moment or activity.
  - *Example: "Virat Kohli batting World Cup", "Formula 1 crash Monza"*
- **Conceptual/Object Shots:** Close-ups of important objects or concepts when people aren't the focus.
  - *Example: "new iPhone 17 design", "vintage film camera close up"*

**3. What to AVOID:**
- **Do not simply use the headline as a query.** It's almost always too specific and will yield no results.
- **Avoid queries that will lead to charts, graphs, or text-heavy infographics.** Focus on photographic results.
- **Avoid overly long or complex queries.** Keep them concise (3-6 words is ideal).
- **Avoid searching for abstract emotions.** Don't search for "sadness"; search for "person looking down rain" which *implies* sadness.

SPECIAL NOTE: THE QUERY MUST MATCH THE GIVEN REFERENCE IMAGE

---

### **Query Generation Strategies & Examples**

#### **Strategy for Factual News Events (Goal: Authenticity)**

**Example Headline:** "Indian Army's Lieutenant Colonel & soldier killed in Ladakh after huge rock falls on military vehicle"
**Analysis:** This is a **Factual News Event**. The goal is to find real photos of this specific incident.
```json
{{
  "queries": [
    "Ladakh military vehicle accident scene",
    "rockfall on military vehicle in Ladakh",
  ]
}}
```
*(Note: These queries are specific and use journalistic keywords to find real event photos.)*

---

#### **Strategy for Entertainment/Features (Goal: Aesthetics & Vibe)**

**Example Headline:** "Kay Kay Menon starrer Special Ops Season 2 shines as fans appreciate acting, storyline and thrill"
**Analysis:** This is **Entertainment News**. The goal is to find a cool, high-impact image. Its an Indian OTT series so use India as a keyword.
```json
{{
  "queries": [
    "Special Ops season 2 poster high resolution India",
    "Kay Kay Menon in Special Ops series India",
  ]
}}
```
*(Note: These queries mix official assets with more conceptual, aesthetic shots.)*

**Example Headline:** "Hyderabad airport launches 'Therapy Dog Program' to ease travel stress"
**Analysis:** This is a **Feature/Lifestyle News** story. The goal is to find a heartwarming, visually appealing photo.
```json
{{
  "queries": [
    "Golden Retriever therapy dog at airport",
    "passengers petting therapy dogs in terminal"
  ]
}}
```
*(Note: These queries focus on capturing the emotion and concept of the story.)*

---

**OUTPUT FORMAT:**
<reasoning>
</reasoning>

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
Query: {}
Image Resolution: {}

**Scoring Criteria:**
- Primary Criteria: 
  - How relevant the image is to the Query and the reference image.
  - Images must be **free of any text**, watermarks etc. 
  NOTE: This rule can be broken if the image is an official poster or teaser of the movie.
  - Images must be **Instagram-worthy** (aesthetic appeal, good lighting, visually engaging)
- Secondary Criteria: 
  - How close the image resolution is to 1080x1350. 
  - NOTE PLEASE AVOID LANDSCAPE IMAGES OR ELSE I WILL FIND YOU AND KILL YOU.
  - If the image is not 1080x1350, then give score based on how centered the image subjects are.

**Output Format:**
<reasoning>
</reasoning>

```json
{{
  "image_score": <number>
}}
```
"""


STORY_BOARD_PROMPT = """
You are an expert social media storyboard writer for the Indian youth media brand, **ScoopWhoop**.

**Your Persona and Style (ScoopWhoop Voice):**
*   **Tone:** Engaging, professional journalist who writes in clear, crisp English.
*   **Audience:** Young Indian millennials and Gen Z.
*   **Formatting:** Use short, punchy sentences. Employ questions, and bold statements to grab attention.

HEADLINE: {}

TEMPLATE: {}

**Your Task:**
1.  **Analyze the provided headline** and the given template.
2.  Search the web for more information about the headline.
3.  Create a storyboard following the given template
4.  Give the output in the following format:

```json
{{
  "storyboard": [
    "<storyboard_slide_1_json_input>",
    "<storyboard_slide_2_json_input>",
    "<storyboard_slide_n_json_input>",
  ]
}}
```

NOTE: 
- KEEP The StoryBoard Concise and straight to the point.
"""
