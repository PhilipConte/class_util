from django.utils.html import format_html

def gen_link(value, link):
    return format_html('<a href={}>{}</a>', link, value)

def sections_stats(sections):
    students = sum([s.class_size for s in sections])
    gpa = float(sum([s.average_GPA * s.class_size / students for s in sections]))
    a = float(sum([s.As * s.class_size / students for s in sections]))
    b = float(sum([s.Bs * s.class_size / students for s in sections]))
    c = float(sum([s.Cs * s.class_size / students for s in sections]))
    d = float(sum([s.Ds * s.class_size / students for s in sections]))
    f = float(sum([s.Fs * s.class_size / students for s in sections]))
    return {'gpa': gpa, 'a': a, 'b': b, 'c': c, 'd': d, 'f': f}