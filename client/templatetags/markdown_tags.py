from django import template
from django.utils.safestring import mark_safe
from django.utils.text import slugify
import markdown as md
import re

register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ''
    
    # Convert markdown to HTML
    html = md.markdown(text, extensions=['fenced_code', 'tables', 'extra'])
    
    # Add IDs to headings for anchor links (h1, h2, and h3)
    def add_heading_ids(match):
        level = match.group(1)
        content = match.group(2)
        # Create slug from heading text for the ID
        heading_id = slugify(content)
        return f'<h{level} id="{heading_id}">{content}</h{level}>'
    
    html = re.sub(r'<h([1-3])>(.+?)</h\1>', add_heading_ids, html)
    
    return mark_safe(f'<div class="markdown">{html}</div>')
