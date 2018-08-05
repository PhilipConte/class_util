from django.template.loader import get_template
from django import template

register = template.Library()

@register.inclusion_tag('tags/stat_view.html')
def stat_view(stats, title):
    return {'title': title + ' Distribution', 'stats': stats}

@register.inclusion_tag('tags/chart.html')
def chart(title, url_name, slug, instructor=None, subtitle=None):
    return {
        'title': title,
        'url_name': url_name,
        'slug': slug,
        'instructor': instructor,
        'subtitle': subtitle
    }

@register.inclusion_tag('tags/chart_loader.html')
def chart_loader():
    pass
