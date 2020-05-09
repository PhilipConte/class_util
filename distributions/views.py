from urllib.parse import unquote

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, TemplateView
from django.http import HttpResponseRedirect
import django_tables2
from .models import Course, Section
from .tables import SectionTable, CourseTable, GroupedSectionTable
from .filters import CourseFilter, CourseFilterMulti, GroupedSectionFilter

class FilteredSingleTableView(django_tables2.SingleTableView):
    filter_class = None

    def get_table_data(self):
        data = self.get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=data)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filter
        return context


class CourseFilteredListView(FilteredSingleTableView):
    model = Course
    table_class = CourseTable
    filter_class = CourseFilter
    template_name ='course_list.html'

    def get(self, request):
        qs = self.get_table_data()
        if qs.count() == 1:
            return HttpResponseRedirect(qs.first().get_absolute_url())
        else:
            return super().get(request)


class CourseListView(CourseFilteredListView):
    filter_class = CourseFilterMulti
    template_name = 'course_list.html'


class CourseSearchView(TemplateView):
    template_name = 'course_search.html'


class CourseDetailView(FilteredSingleTableView):
    model = Section
    table_class = GroupedSectionTable
    filter_class = GroupedSectionFilter
    template_name = 'course_detail.html'

    def get_queryset(self):
        self.course = get_object_or_404(Course, slug=self.kwargs['slug'])
        return self.course.sections.group_by_instructor()

    def get_table_kwargs(self):
        return {
            'request': self.request,
            'slug': self.course.slug}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] =  self.course
        return context

class CourseInstructorDetailView(django_tables2.SingleTableView):
    model = Section
    table_class = SectionTable
    template_name = 'course_instructor_detail.html'

    def get_queryset(self):
        self.course = get_object_or_404(Course, slug=self.kwargs['slug'])
        self.instructor = unquote(self.kwargs['instructor'])
        return self.course.sections.filter(instructor=self.instructor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] =  self.course
        context['instructor'] = self.instructor
        return context
