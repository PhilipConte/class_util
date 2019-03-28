from django.urls import reverse
import django_tables2 as tables
from . import models as m

from .utils import gen_link, quote

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
        template_name = 'django_tables2/bootstrap.html'
        fields = ['department', 'number', 'title', 'hours', *GRADES]
    
    title = tables.LinkColumn()
    average_GPA = RoundColumn(2)
    As = RoundColumn(verbose_name='A%')
    Bs = RoundColumn(verbose_name='B%')
    Cs = RoundColumn(verbose_name='C%')
    Ds = RoundColumn(verbose_name='D%')
    Fs = RoundColumn(verbose_name='F%')

class SectionTable(tables.Table):
    class Meta:
        model = m.Section
        template_name = 'django_tables2/bootstrap.html'
        fields= ['term', 'course', 'CRN', 'instructor', *GRADES, 'withdrawals', 'class_size']

    course = tables.RelatedLinkColumn(attrs={'target': '_blank'})
    instructor = tables.LinkColumn()

class GroupedSectionTable(tables.Table):
    def __init__(self, *args, **kwargs):
        temp_course_args = kwargs.pop("course_args")
        super().__init__(*args, **kwargs)
        self.course_args = temp_course_args
    
    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = m.Section
        fields = ['instructor', 'sections_taught', 'withdrawals', *GRADES]
    
    term = tables.Column()
    instructor = tables.Column()
    sections_taught = tables.Column()
    average_GPA = RoundColumn(2)
    As = RoundColumn(verbose_name='A%')
    Bs = RoundColumn(verbose_name='B%')
    Cs = RoundColumn(verbose_name='C%')
    Ds = RoundColumn(verbose_name='D%')
    Fs = RoundColumn(verbose_name='F%')
    def render_instructor(self, value):
        return gen_link(value, reverse('distributions:course_instructor_detail', args=[*self.course_args, quote(value)]))
