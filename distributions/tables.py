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

    gpa = tables.Column(verbose_name='Average GPA')
    stats = tables.Column(orderable=False)

    def render_stats(self, record):
        return pretty_dict(removekey(record.stats, 'GPA'))

class SectionTable(tables.Table):
    class Meta:
        model = m.Section
        template_name = 'django_tables2/bootstrap.html'
        exclude= 'id'

    course = tables.RelatedLinkColumn(attrs={'target': '_blank'})
    instructor = tables.Column()
    def render_instructor(self, record, value):
        return gen_link(value, reverse('course_instructor', args=[*record.course.url_args, quote(record.instructor)]))
