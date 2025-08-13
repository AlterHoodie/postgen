from src.templates.timeline import timeline_template
from src.templates.thumbnail import thumbnail_template
from src.templates.writeup import writeup_template
from src.templates.text_based import text_based_template
from src.templates.meme import meme_template

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
