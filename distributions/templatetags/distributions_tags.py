from django.template.loader import get_template
from django import template

from distributions.utils import sections_stats

register = template.Library()

def average_sections(sections, title):
    return {'title': title + ' Distribution', 'stats': sections_stats(sections)}

register.inclusion_tag(get_template('tags/average_sections.html'))(average_sections)
