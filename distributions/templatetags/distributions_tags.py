from django.template.loader import get_template
from django import template

register = template.Library()

@register.inclusion_tag('tags/form_button.html')
def form_button(glyph):
    return {'glyph': glyph}

@register.inclusion_tag('tags/chart.html')
def chart(title, url_name, slug, instructor=None):
    return {
        'title': title,
        'url_name': url_name,
        'slug': slug,
        'instructor': instructor,
    }

@register.inclusion_tag('tags/chart_loader.html')
def chart_loader():
    pass

@register.inclusion_tag('tags/search_bar.html')
def search_bar():
    from ..filters import CourseFilterMulti
    return {'form': CourseFilterMulti().form }

@register.filter
def joinBy(value, arg):
    return arg.join(value)

@register.filter
def dictGet(dictionary, args):
    args = args.split(',')
    key = args[0]
    try:
        fallback = args[1]
    except:
        fallback = None

    return dictionary.get(key, fallback)
