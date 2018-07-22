from django.template.loader import get_template
from django import template

register = template.Library()

def stat_view(stats, title):
    return {'title': title + ' Distribution', 'stats': stats}

register.inclusion_tag(get_template('tags/stat_view.html'))(stat_view)
