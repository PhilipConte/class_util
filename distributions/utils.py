from urllib.parse import quote as og_quote

from django.utils.html import format_html
from django.urls import reverse

def gen_link(value, link):
    return format_html('<a href={}>{}</a>', link, value)

def link_reverse(value): return gen_link(value, reverse(value.lower()))

def pretty_dict(dic):
    return '    '.join([(str(key) + ': ' + str(dic[key]))  for key in dic])

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def quote(value): return og_quote(value, safe='')
