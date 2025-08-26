from src.templates.scoopwhoop.timeline import timeline_template
from src.templates.scoopwhoop.thumbnail import thumbnail_template
from src.templates.scoopwhoop.writeup import writeup_template
from src.templates.scoopwhoop.text_based import text_based_template
from src.templates.scoopwhoop.meme import meme_template

def get_template_config(template_type: str) -> dict:
    """Get template configuration based on type"""
    if template_type == "timeline":
        return timeline_template
    elif template_type == "thumbnail":
        return thumbnail_template
    elif template_type == "writeup":
        return writeup_template
    elif template_type == "text_based":
        return text_based_template
    elif template_type == "meme":
        return meme_template
    else:
        raise ValueError(f"Unknown template type: {template_type}")
