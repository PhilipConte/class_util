from urllib.parse import unquote

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
import django_tables2
from .models import Course, Section, Term
from .tables import SectionTable, CourseTable, GroupedSectionTable
from .filters import SectionFilter, CourseFilter, CourseFilterMulti, SectionGroupedByInstructorFilter

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
    template_name = 'course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hierarchy'] = [{'text': 'Sections'}, {'text': 'Filtered'}]
        return context

class CourseFilteredListView(FilteredSingleTableView):
    model = Course
    table_class = CourseTable
    filter_class = CourseFilter
    template_name ='course_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hierarchy'] = [
            {'text': 'Courses', 'link': reverse('distributions:course_list')},
            {'text': 'Filtered'},
        ]
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
        context['hierarchy'] = [{'text': 'Courses'}]
        print(len(self.filter.filters))
        return context

class CourseSearchView(TemplateView):
    template_name = 'course_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hierarchy'] = [
            {'text': 'Courses', 'link': reverse('distributions:course_list')},
            {'text': 'Search'},
        ]
        print("TERM ID" + str(self.request.session.get('term_id', 'fail')))
        return context

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
        context['hierarchy'] = [
            {'text': 'Courses', 'link': reverse('distributions:course_list')},
            {'text': self.course.short()},
        ]
        context['title'] = self.course.html()
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
        context['hierarchy'] = [
            {'text': 'Courses', 'link': reverse('distributions:course_list')},
            {'text': self.course.short(), 'link': self.course.get_absolute_url()},
            {'text': self.instructor},
        ]
        context['title'] = '<strong>' + self.course.short() \
            + '</strong>: Statistics for Professor ' + self.instructor
        context['course'] =  self.course
        context['course_sections'] = self.course_sections
        context['instructor'] = self.instructor
        context['sections'] =  self.sections
        return context

def set_term(request, term_id):
    request.session['term_id'] = get_object_or_404(Term, id=term_id).id
    return redirect(request.META.get('HTTP_REFERER'))
