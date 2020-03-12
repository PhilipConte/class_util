from django.utils.html import format_html
from django.urls import reverse
import django_tables2 as tables
from . import models as m

GRADES = ['average_GPA', 'As', 'Bs', 'Cs', 'Ds', 'Fs']


class CourseTable(tables.Table):
    class Meta:
        model = m.Course
        fields = ['department', 'number', 'title', 'hours', *GRADES]
    
    title = tables.Column(linkify=True)


class SectionTable(tables.Table):
    class Meta:
        model = m.Section
        fields= ['term', 'CRN', *GRADES, 'withdrawals', 'class_size']


class GroupedSectionTable(tables.Table):
    def __init__(self, *args, **kwargs):
        slug = kwargs.pop("slug")
        super().__init__(*args, **kwargs)
        self.slug = slug
    
    class Meta:
        model = m.Section
        fields = ['instructor', 'sections_taught', 'withdrawals', *GRADES]

    def render_instructor(self, value):
        return format_html('<a href={}>{}</a>',
            reverse('distributions:course_instructor_detail', args=[
                self.slug, value]),
            value)
