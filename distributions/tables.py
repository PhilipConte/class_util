from django.utils.html import format_html
from django.urls import reverse
from django_tables2.utils import A
import django_tables2 as tables
from . import models as m

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

    course = tables.RelatedLinkColumn(attrs={'target': '_blank'})
    instructor = tables.LinkColumn('course_instructor', args=[A('course.department'), A('course.number'), A('course.title'), A('course.hours'), A('instructor')])
