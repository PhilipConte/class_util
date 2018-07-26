from urllib.parse import unquote

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Count, Sum, Avg, Value, CharField, PositiveIntegerField
import django_tables2
from .models import Course, Section
from .tables import SectionTable, CourseTable, GroupedSectionTable
from .filters import SectionFilter, CourseFilter
from .utils import gen_link, link_reverse

class FilteredSingleTableView(django_tables2.SingleTableView):
    filter_class = None

    def get_table_data(self):
        data = super(FilteredSingleTableView, self).get_table_data()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(FilteredSingleTableView, self).get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

class SectionFilteredSingleTableView(FilteredSingleTableView):
    model = Section
    table_class = SectionTable
    filter_class = SectionFilter
    template_name='section_table.html'

    def get_context_data(self, **kwargs):
        context = super(SectionFilteredSingleTableView, self).get_context_data(**kwargs)
        context['header'] = link_reverse('Sections') + '/Filter'
        return context

class SectionSingleTableView(django_tables2.SingleTableView):
    model = Section
    table_class = SectionTable
    template_name='section_table.html'

    def get_context_data(self, **kwargs):
        context = super(SectionSingleTableView, self).get_context_data(**kwargs)
        context['header'] = 'Sections'
        return context

class CourseFilteredSingleTableView(FilteredSingleTableView):
    model = Course
    table_class = CourseTable
    filter_class = CourseFilter
    template_name='course_table.html'

    def get_context_data(self, **kwargs):
        context = super(CourseFilteredSingleTableView, self).get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/Filter'
        return context

class CourseSingleTableView(django_tables2.SingleTableView):
    model = Course
    table_class = CourseTable
    template_name='course_table.html'

    def get_context_data(self, **kwargs):
        context = super(CourseSingleTableView, self).get_context_data(**kwargs)
        context['header'] = 'Courses'
        return context

def course_shortcut(request, department, number):
    department = department.upper()
    try:
        course = Course.objects.get(department=department, number=number)
        return redirect(course)
    except Course.MultipleObjectsReturned:
        courses = Course.objects.all().filter(department=department, number=number)
        table = CourseTable(sections, request=request)
        header = link_reverse('Courses') + '/' + department + ' ' + number
        return render(request, 'course_shortcut.html', {'header': header, 'department': department, 'number': number, 'table': table})

def course(request, department, number, title, hours):
    department = department.upper()
    title=unquote(title)
    course = Course.objects.get(department=department, number=number, title=title, hours=hours)
    sections = course.sections.all()
    group = course.sections.values('instructor').annotate(
            num=Count('instructor'), withdrawals=Sum('withdrawals'),
            average_GPA=Avg('average_GPA'), As=Avg('As'), Bs=Avg('Bs'),
            Cs=Avg('Cs'), Ds=Avg('Ds'), Fs=Avg('Fs'))#,
    table = GroupedSectionTable(group, request=request, course_args=course.url_args)
    context = {'header': link_reverse('Courses') + '/' + course.short(),
        'course': course, 'sections': sections, 'table': table,}
    return render(request, 'course.html', context)

def course_instructor(request, department, number, title ,hours, instructor):
    department = department.upper()
    title=unquote(title)
    instructor=unquote(instructor)
    course = Course.objects.get(department=department, number=number, title=title, hours=hours)
    course_sections = course.sections.all()
    sections = course_sections.filter(instructor=instructor)
    table = SectionTable(sections, exclude=['id', 'course', 'instructor'], request=request)
    header = link_reverse('Courses') + '/' + gen_link(course.short(), course.get_absolute_url()) + '/' + instructor
    return render(request, 'course_instructor.html',
        {'header': header, 'course': course, 'instructor': instructor,
        'table': table, 'sections': sections, 'course_sections': course_sections})
