from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Section
from .tables import SectionTable
from .filters import SectionFilter
import django_tables2

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

class SectionSingleTableView(django_tables2.SingleTableView):
    model = Section
    table_class = SectionTable
    template_name='section_table.html'

    def get_context_data(self, **kwargs):
        context = super(SectionSingleTableView, self).get_context_data(**kwargs)
        context['header'] = 'All Sections'
        return context


def course_shortcut(request, department, number):
    department = department.upper()
    try:
        course = Course.objects.get(department=department, number=number)
        return redirect(course)
    except Course.MultipleObjectsReturned:
        courses = Course.objects.all().filter(department=department, number=number)
        table = CourseTable(sections, request=request)
        return render(request, 'course_shortcut.html', {'department': department, 'number': number, 'table': table})

def course(request, department, number, title, hours):
    department = department.upper()
    course = Course.objects.get(department=department, number=number, title=title, hours=hours)
    sections = Section.objects.all().filter(course=course)
    table = SectionTable(sections, exclude=['id', 'course'], request=request)
    return render(request, 'course.html', {'course': course, 'table': table})

def course_instructor(request, department, number, title ,hours, instructor):
    department = department.upper()
    course = Course.objects.get(department=department, number=number, title=title, hours=hours)
    sections = Section.objects.all().filter(course=course, instructor=instructor)
    table = SectionTable(sections, exclude=['id', 'course', 'instructor'], request=request)
    return render(request, 'course_instructor.html', {'course': course, 'instructor': instructor, 'table': table})
