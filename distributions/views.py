from urllib.parse import unquote

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
import django_tables2
from .models import Course, Section, stats_dict
from .tables import SectionTable, CourseTable, GroupedSectionTable
from .filters import SectionFilter, CourseFilter, CourseFilterMulti
from .utils import gen_link, link_reverse, dict_pop

class FilteredSingleTableView(django_tables2.SingleTableView):
    filter_class = None

    def get_table_data(self):
        data = super().get_table_data()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context

class SectionFilteredSingleTableView(FilteredSingleTableView):
    model = Section
    table_class = SectionTable
    filter_class = SectionFilter
    template_name = 'section_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Sections') + '/Filter'
        return context

class SectionSingleTableView(django_tables2.SingleTableView):
    model = Section
    table_class = SectionTable
    template_name = 'section_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Sections'
        return context

class CourseFilteredSingleTableView(FilteredSingleTableView):
    model = Course
    table_class = CourseTable
    filter_class = CourseFilter
    template_name ='course_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/Filter'
        return context

class CourseSingleTableView(django_tables2.SingleTableView):
    model = Course
    table_class = CourseTable
    template_name = 'course_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Courses'
        return context

class CourseMultiFilteredSingleTableView(CourseFilteredSingleTableView):
    filter_class = CourseFilterMulti
    template_name = 'course_search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/Search Results'
        return context

class CourseSearch(TemplateView):
    template_name = 'course_search.html'
    filter_class = CourseFilterMulti

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/Search'
        context['filter'] = self.filter_class(self.request.GET, queryset=Course.objects.all())
        return context

    def get(self, request):
        def custom_redirect(url_name, *args, **kwargs):
            import urllib
            url = reverse(url_name, args = args)
            params = urllib.parse.urlencode(kwargs)
            return HttpResponseRedirect(url + "?%s" % params)
        if (len(request.GET) and len([c for c in request.GET.values()][0])):
            return custom_redirect('courses_search_results', **request.GET.dict())
        return super().get(self, request)

def course(request, department, number, title, hours):
    department = department.upper()
    title=unquote(title)
    course = Course.objects.get(department=department, number=number, title=title, hours=hours)
    sections = course.sections.all()
    group = sections.group_by_instructor()
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
