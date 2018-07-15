from urllib.parse import quote as og_quote

from django.utils.html import format_html
from django.urls import reverse

def gen_link(value, link):
    return format_html('<a href={}>{}</a>', link, value)

def link_reverse(value): return gen_link(value, reverse(value.lower()))

def sections_stats(sections):
    withdrawals = sum([s.withdrawals for s in sections])
    students = sum([s.class_size for s in sections])
    gpa = round(float(sum([s.average_GPA * s.class_size / students for s in sections])), 2)
    a = round(float(sum([s.As * s.class_size / students for s in sections])), 2)
    b = round(float(sum([s.Bs * s.class_size / students for s in sections])), 2)
    c = round(float(sum([s.Cs * s.class_size / students for s in sections])), 2)
    d = round(float(sum([s.Ds * s.class_size / students for s in sections])), 2)
    f = round(float(sum([s.Fs * s.class_size / students for s in sections])), 2)
    return {'GPA': gpa, 'A': a, 'B': b, 'C': c, 'D': d, 'F': f, 'Students': students, 'Withdrawals': withdrawals}

def pretty_dict(dict):
    return '    '.join([(str(key) + ': ' + str(dict[key]))  for key in dict])

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def quote(value): return og_quote(value, safe='')
