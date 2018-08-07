from urllib.parse import quote as og_quote

from django.utils.html import format_html

def gen_link(value, link):
    return format_html('<a href={}>{}</a>', link, value)

def dict_pop(d, to_pop):
    if type(d) is not dict:
        raise TypeError('first arg must be dict')
    if type(to_pop) is str:
        to_pop = [to_pop]
    elif type(to_pop) is not list or set([type(i) is str for i in to_pop]) != set([True]):
        raise TypeError('type must be (list of) str(s)')
    r = dict(d)
    for key in to_pop:
        del r[key]
    return r

def quote(value): return og_quote(value, safe='')
