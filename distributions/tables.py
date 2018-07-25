from django.utils.html import format_html
from django.urls import reverse
from django_tables2.utils import A
import django_tables2 as tables
from . import models as m

from .utils import pretty_dict, removekey, gen_link, quote

class CourseTable(tables.Table):
    class Meta:
        model = m.Course
        template_name = 'django_tables2/bootstrap.html'
        exclude = 'id'
    
    link = tables.LinkColumn(None, text='link')

    average_GPA = tables.Column()
    stats = tables.Column(orderable=False)

    def render_average_GPA(self, value):
        return round(value, 2)

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
