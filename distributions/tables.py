from django.utils.html import format_html
from django.urls import reverse
from django_tables2.utils import A
import django_tables2 as tables
from . import models as m

from .utils import pretty_dict, removekey, gen_link, quote

class RoundColumn(tables.Column):
    def __init__(self, decimals=1):
        super().__init__()
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
    stats = tables.Column(orderable=False)

    def render_stats(self, value):
        return pretty_dict(removekey(value, 'GPA'))

class SectionTable(tables.Table):
    class Meta:
        model = m.Section
        template_name = 'django_tables2/bootstrap.html'
        exclude= 'id'

    course = tables.RelatedLinkColumn(attrs={'target': '_blank'})
    instructor = tables.Column()
    def render_instructor(self, record, value):
        return gen_link(value, reverse('course_instructor', args=[*record.course.url_args, quote(record.instructor)]))

class GroupedSectionTable(tables.Table):
    course_args = None

    def __init__(self, *args, **kwargs):
        temp_course_args = kwargs.pop("course_args")
        super().__init__(*args, **kwargs)
        self.course_args = temp_course_args
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = m.Section
        exclude= ['id', 'course', 'class_size', 'CRN', 'term']
    
    instructor = tables.Column()
    average_GPA = RoundColumn(2)
    As = RoundColumn()
    Bs = RoundColumn()
    Cs = RoundColumn()
    Ds = RoundColumn()
    Fs = RoundColumn()
    def render_instructor(self, value):
        return gen_link(value, reverse('course_instructor', args=[*self.course_args, quote(value)]))
