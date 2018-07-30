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

class SectionFilteredListView(FilteredSingleTableView):
    model = Section
    table_class = SectionTable
    filter_class = SectionFilter
    template_name = 'section_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Sections') + '/Filter'
        return context

class SectionListView(django_tables2.SingleTableView):
    model = Section
    table_class = SectionTable
    template_name = 'section_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Sections'
        return context

class CourseFilteredListView(FilteredSingleTableView):
    model = Course
    table_class = CourseTable
    filter_class = CourseFilter
    template_name ='course_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/Filter'
        return context

class CourseListView(django_tables2.SingleTableView):
    model = Course
    table_class = CourseTable
    template_name = 'course_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Courses'
        return context

class CourseMultiFilteredListView(CourseFilteredListView):
    filter_class = CourseFilterMulti
    template_name = 'course_search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/Search Results'
        return context

class CourseSearchView(TemplateView):
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

class CourseDetailView(django_tables2.SingleTableView):
    model = Section
    table_class = GroupedSectionTable
    template_name = 'course.html'    

    def parse_params(self):
        self.course = get_object_or_404(Course,
            department=self.kwargs['department'].upper(),
            number=self.kwargs['number'],
            title=unquote(self.kwargs['title']), hours=self.kwargs['hours'])
        self.sections = self.course.sections.all()

    def get_table_data(self):
        return self.sections.group_by_instructor()

    def get_table_kwargs(self):
        return {
            'request': self.request,
            'course_args': self.course.url_args}

    def get_context_data(self, **kwargs):
        self.parse_params()

        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/' + self.course.short()
        context['course'] =  self.course
        context['sections'] =  self.sections
        return context

class CourseInstructorDetailView(django_tables2.SingleTableView):
    model = Section
    table_class = SectionTable
    template_name = 'course_instructor.html'    

    def parse_params(self):
        self.course = get_object_or_404(Course,
            department=self.kwargs['department'].upper(),
            number=self.kwargs['number'],
            title=unquote(self.kwargs['title']), hours=self.kwargs['hours'])
        self.course_sections = self.course.sections.all()
        self.instructor = unquote(self.kwargs['instructor'])
        self.sections = self.course_sections.filter(
            instructor=self.instructor)

    def get_table_data(self):
        return self.sections

    def get_table_kwargs(self):
        return {
            'request': self.request,
            'exclude': ['id', 'course', 'instructor']}

    def get_context_data(self, **kwargs):
        self.parse_params()

        context = super().get_context_data(**kwargs)
        context['header'] = link_reverse('Courses') + '/' + gen_link(self.course.short(), self.course.get_absolute_url()) + '/' + self.instructor
        context['course'] =  self.course
        context['course_sections'] = self.course_sections
        context['instructor'] = self.instructor
        context['sections'] =  self.sections
        return context
