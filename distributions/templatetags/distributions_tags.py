from django import template
from distributions.filters import CourseFilterMulti

register = template.Library()

@register.inclusion_tag('tags/chart.html')
def chart(title, url_name, slug, instructor=None):
    return {
        'title': title,
        'url_name': url_name,
        'slug': slug,
        'instructor': instructor,
    }

@register.inclusion_tag('tags/search_bar.html')
def search_bar():
    return {'form': CourseFilterMulti().form }
