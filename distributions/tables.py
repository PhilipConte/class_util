from django.utils.html import format_html
from django.urls import reverse
from django_tables2.utils import A
import django_tables2 as tables
from . import models as m

def link_format(value, link):
    return format_html('<a href={} target="_blank">{}</a>', link, value)

class CourseTable(tables.Table):
    class Meta:
        model = m.Course
        template_name = 'django_tables2/bootstrap.html'
        exclude = 'id'
    
    Link = tables.LinkColumn(None, text='link')

class SectionTable(tables.Table):
    class Meta:
        model = m.Section
        template_name = 'django_tables2/bootstrap.html'
        exclude= 'id'

    course = tables.Column()
    def render_course(self, value):
        return link_format(value, value.get_absolute_url())
