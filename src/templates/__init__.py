from src.templates.scoopwhoop.timeline import timeline_template
from src.templates.scoopwhoop.thumbnail import thumbnail_template as scoopwhoop_thumbnail_template
from src.templates.scoopwhoop.writeup import writeup_template
from src.templates.scoopwhoop.text_based import text_based_template as scoopwhoop_text_based_template
from src.templates.scoopwhoop.meme import meme_template

from src.templates.twitter.tweet_image import tweet_image_template
from src.templates.twitter.tweet_text import tweet_text_template

from src.templates.social_village.content import content_template
from src.templates.social_village.thumbnail import thumbnail_template as social_village_thumbnail_template

from src.templates.the_sarcastic_indian.writeup import writeup_template as sarcastic_writeup_template

from src.templates.infomance.content import infomance_content_template
from src.templates.infomance.thumbnail import infomance_thumbnail_template
from src.templates.infomance.thumbnail_3 import infomance_thumbnail_3_template

def get_template_config(template_type: str, page_name: str) -> dict:
    """Get template configuration based on type"""
    if page_name == "scoopwhoop":
        if template_type == "timeline":
            return timeline_template
        elif template_type == "thumbnail":
            return scoopwhoop_thumbnail_template
        elif template_type == "writeup":
            return writeup_template
        elif template_type == "text_based":
            return scoopwhoop_text_based_template
        elif template_type == "meme":
            return meme_template
        else:
            raise ValueError(f"Unknown template type for given {page_name}: {template_type}")
    elif page_name == "twitter":
        if template_type == "tweet_image":
            return tweet_image_template
        elif template_type == "text_based":
            return tweet_text_template
        else:
            raise ValueError(f"Unknown template type for given {page_name}: {template_type}")
    
    elif page_name == "social_village":
        if template_type == "content":
            return content_template
        elif template_type == "thumbnail":
            return social_village_thumbnail_template
        else:
            raise ValueError(f"Unknown template type for given {page_name}: {template_type}")
    
    elif page_name == "the_sarcastic_indian":
        if template_type == "writeup":
            return sarcastic_writeup_template
        else:
            raise ValueError(f"Unknown template type for given {page_name}: {template_type}")
    
    elif page_name == "infomance":
        if template_type == "content":
            return infomance_content_template
        elif template_type == "thumbnail":
            return infomance_thumbnail_template
        elif template_type == "thumbnail_3":
            return infomance_thumbnail_3_template
        else:
            raise ValueError(f"Unknown template type for given {page_name}: {template_type}")
    else:
        raise ValueError(f"Unknown page name: {page_name}")
        
