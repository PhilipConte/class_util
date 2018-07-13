from django.utils.html import format_html

def gen_link(value, link):
    return format_html('<a href={}>{}</a>', link, value)
