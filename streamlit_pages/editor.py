import streamlit as st
from typing import Dict, Tuple
from src.workflows.editors import text_editor
from src.utils import extract_text_from_html

def text_editor_form(text_values: Dict, image_bytes: bytes, template: Dict, 
                           slide_name: str, form_key: str) -> Tuple[bytes, bool]:
    """
    Simple Streamlit form for text editing using text_editor from editors.py
    
    Args:
        text_json: Text template configuration 
        image_bytes: Original image bytes
        template: Template configuration
        slide_name: Slide name
        form_key: Unique form key
        
    Returns:
        (new_image_bytes, submitted)
    """
    text_json = template['slides'][slide_name]['text_json']
    with st.form(key=form_key):
        text_input = {}
        
        # Create inputs based on text_json
        for field_name, config in text_json.get('text_template', {}).items():
            display_name = field_name.replace('_', ' ').title()
            
            if config.get('type') == 'checkbox':
                text_input[field_name] = st.checkbox(display_name,value=True if text_values.get(field_name) else False)
            elif config.get('type') == 'text_area':
                text_input[field_name] = st.text_area(f"{display_name}:",value=extract_text_from_html(text_values.get(field_name)))
            elif config.get('type') == 'text':
                text_input[field_name] = st.text_input(f"{display_name}:",value=extract_text_from_html(text_values.get(field_name)))
        
        submitted = st.form_submit_button("Generate New Image", type="primary")
        
        if submitted:
            try:
                new_image_bytes = text_editor(template, slide_name, text_input, image_bytes)
                return new_image_bytes, True
            except Exception as e:
                st.error(f"Error: {e}")
                return None, False
        
        return None, False