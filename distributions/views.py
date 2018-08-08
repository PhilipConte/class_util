from urllib.parse import unquote, urlencode

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
import django_tables2
from .models import Course, Section
from .tables import SectionTable, CourseTable, GroupedSectionTable
from .filters import SectionFilter, CourseFilter, CourseFilterMulti, SectionGroupedByInstructorFilter
from .utils import gen_link

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
    template_name = 'filtered_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Sections/Filter'
        context['title'] = 'Filtered Sections'
        return context

class CourseFilteredListView(FilteredSingleTableView):
    model = Course
    table_class = CourseTable
    filter_class = CourseFilter
    template_name ='filtered_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = gen_link('Courses', reverse('distributions:course_list'))  + '/Filter'
        context['title'] = 'Filtered Courses'
        return context

    def get(self, request):
        qs = self.get_table_data()
        if qs.count() == 1:
            print('1 item')
            return HttpResponseRedirect(qs.first().get_absolute_url()) 
        else:
            return super().get(request)

class CourseListView(CourseFilteredListView):
    filter_class = CourseFilterMulti
    template_name = 'course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Courses'
        return context

class CourseSearchView(TemplateView):
    template_name = 'course_search.html'
    filter_class = CourseFilterMulti

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = gen_link('Courses', reverse('distributions:course_list')) + '/Search'
        context['filter'] = self.filter_class(self.request.GET, queryset=Course.objects.all())
        return context

    def get(self, request):
        def custom_redirect(url_name, *args, **kwargs):
            url = reverse(url_name, args = args)
            params = urlencode(kwargs)
            return HttpResponseRedirect(url + "?%s" % params)

        if (len(request.GET) and len(list(request.GET.values())[0])):
            return custom_redirect('distributions:course_list', **request.GET.dict())
        return super().get(self, request)

class CourseDetailView(FilteredSingleTableView):
    model = Section
    table_class = GroupedSectionTable
    filter_class = SectionGroupedByInstructorFilter
    template_name = 'course_detail.html'    

    def parse_params(self):
        self.course = get_object_or_404(Course,
            slug=self.kwargs['slug'])
        self.sections = self.course.sections.all()

    def get_table_data(self):
        data = self.sections.group_by_instructor()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_table_kwargs(self):
        return {
            'request': self.request,
            'course_args': [self.course.slug]}

    def get_context_data(self, **kwargs):
        self.parse_params()

        context = super().get_context_data(**kwargs)
        context['header'] = gen_link('Courses', reverse('distributions:course_list')) + '/' + self.course.short()
        context['course'] =  self.course
        context['sections'] =  self.sections
        return context

class CourseInstructorDetailView(django_tables2.SingleTableView):
    model = Section
    table_class = SectionTable
    template_name = 'course_instructor_detail.html'    

    def parse_params(self):
        self.course = get_object_or_404(Course,
            slug=self.kwargs['slug'])
        self.course_sections = self.course.sections.all()
        self.instructor = unquote(self.kwargs['instructor'])
        self.sections = self.course_sections.filter(
            instructor=self.instructor)

    def get_table_data(self):
        return self.sections

    def get_table_kwargs(self):
        return {
            'request': self.request,
            'exclude': ['id', 'course', 'instructor', 'slug']}

    def get_context_data(self, **kwargs):
        self.parse_params()

        context = super().get_context_data(**kwargs)
        context['header'] = gen_link('Courses', reverse('distributions:course_list')) + '/' + gen_link(self.course.short(), self.course.get_absolute_url()) + '/' + self.instructor
        context['course'] =  self.course
        context['course_sections'] = self.course_sections
        context['instructor'] = self.instructor
        context['sections'] =  self.sections
        return context
