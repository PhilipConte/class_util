from urllib.parse import quote
from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables
from . import models as m

GRADES = ['average_GPA', 'As', 'Bs', 'Cs', 'Ds', 'Fs']

class RoundColumn(tables.Column):
    def __init__(self, decimals=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.decimals = decimals

    def render(self, value):
        return round(value, self.decimals)

class CourseTable(tables.Table):
    class Meta:
        model = m.Course
        fields = ['department', 'number', 'title', 'hours', *GRADES]
    
    title = tables.Column(linkify=True)
    average_GPA = RoundColumn(2)
    As = RoundColumn(verbose_name='A%')
    Bs = RoundColumn(verbose_name='B%')
    Cs = RoundColumn(verbose_name='C%')
    Ds = RoundColumn(verbose_name='D%')
    Fs = RoundColumn(verbose_name='F%')

class SectionTable(tables.Table):
    class Meta:
        model = m.Section
        fields= ['term', 'course', 'CRN', 'instructor', *GRADES, 'withdrawals', 'class_size']

    course = tables.Column(linkify=True)
    instructor = tables.Column(linkify=True)

class GroupedSectionTable(tables.Table):
    def __init__(self, *args, **kwargs):
        temp_course_args = kwargs.pop("course_args")
        super().__init__(*args, **kwargs)
        self.course_args = temp_course_args
    
    class Meta:
        model = m.Section
        fields = ['instructor', 'sections_taught', 'withdrawals', *GRADES]
    
    instructor = tables.Column()
    average_GPA = RoundColumn(2)
    As = RoundColumn(verbose_name='A%')
    Bs = RoundColumn(verbose_name='B%')
    Cs = RoundColumn(verbose_name='C%')
    Ds = RoundColumn(verbose_name='D%')
    Fs = RoundColumn(verbose_name='F%')

    def render_instructor(self, value):
        return format_html('<a href={}>{}</a>',
            reverse('distributions:course_instructor_detail', args=[
                *self.course_args, quote(value, safe='')]),
            value)
