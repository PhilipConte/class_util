from django.template.loader import get_template
from django import template

register = template.Library()

def average_sections(sections, title):
    students = sum([s.class_size for s in sections])
    gpa = float(sum([s.average_GPA * s.class_size / students for s in sections]))
    a = float(sum([s.As * s.class_size / students for s in sections]))
    b = float(sum([s.Bs * s.class_size / students for s in sections]))
    c = float(sum([s.Cs * s.class_size / students for s in sections]))
    d = float(sum([s.Ds * s.class_size / students for s in sections]))
    f = float(sum([s.Fs * s.class_size / students for s in sections]))
    return {'title': title + ' Distribution', 'stats': {'gpa': gpa, 'a': a, 'b': b, 'c': c, 'd': d, 'f': f}}

register.inclusion_tag(get_template('tags/average_sections.html'))(average_sections)
