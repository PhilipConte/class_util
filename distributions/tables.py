from django.utils.html import format_html
from django.urls import reverse
from django_tables2.utils import A
import django_tables2 as tables
from . import models as m

from .utils import pretty_dict, dict_pop, gen_link, quote

class RoundColumn(tables.Column):
    def __init__(self, decimals=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = decimals

    def render(self, value):
        return round(value, self.decimals)

class CourseTable(tables.Table):
    class Meta:
        model = m.Course
        template_name = 'django_tables2/bootstrap.html'
        exclude = 'id'
    
    title = tables.LinkColumn(None)
    average_GPA = RoundColumn(2)
    As = RoundColumn(verbose_name='A%')
    Bs = RoundColumn(verbose_name='B%')
    Cs = RoundColumn(verbose_name='C%')
    Ds = RoundColumn(verbose_name='D%')
    Fs = RoundColumn(verbose_name='F%')

    def render_stats(self, value):
        return pretty_dict(dict_pop(value, 'average_GPA'))

class SectionTable(tables.Table):
    class Meta:
        model = m.Section
        template_name = 'django_tables2/bootstrap.html'
        exclude= 'id'

    term = tables.Column(order_by=('term__year', '-term__semester'))
    course = tables.RelatedLinkColumn(attrs={'target': '_blank'})
    instructor = tables.Column()
    def render_instructor(self, record, value):
        return gen_link(value, reverse('course_instructor', args=[*record.course.url_args, quote(record.instructor)]))

class GroupedSectionTable(tables.Table):
    def __init__(self, *args, **kwargs):
        temp_course_args = kwargs.pop("course_args")
        super().__init__(*args, **kwargs)
        self.course_args = temp_course_args
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = m.Section
        exclude = ['id', 'course', 'class_size', 'CRN', 'term']
        sequence = ['instructor', 'sections_taught', 'withdrawals', 'average_GPA', 'As', 'Bs', 'Cs', 'Ds', 'Fs', '...']
    
    term = tables.Column(order_by=('term__year', '-term__semester'))
    instructor = tables.Column()
    sections_taught = tables.Column()
    average_GPA = RoundColumn(2)
    As = RoundColumn(verbose_name='A%')
    Bs = RoundColumn(verbose_name='B%')
    Cs = RoundColumn(verbose_name='C%')
    Ds = RoundColumn(verbose_name='D%')
    Fs = RoundColumn(verbose_name='F%')
    def render_instructor(self, value):
        return gen_link(value, reverse('course_instructor', args=[*self.course_args, quote(value)]))
