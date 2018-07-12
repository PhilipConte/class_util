from urllib.parse import unquote
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django_tables2 import RequestConfig
from .models import Course, Section
from .tables import SectionTable

def table(request):
    sections = Section.objects.all()
    table = SectionTable(sections)
    RequestConfig(request).configure(table)
    return render(request, 'table.html', {'table': table})

def course_shortcut(request, department, number):
    department = department.upper()
    try:
        course = Course.objects.get(department=department, number=number)
        return redirect(course)
    except Course.MultipleObjectsReturned:
        courses = Course.objects.all().filter(department=department, number=number)
        table = CourseTable(sections)
        RequestConfig(request).configure(table)
        return render(request, 'course_shortcut.html', {'department': department, 'number': number, 'table': table})

def course(request, department, number, title, hours):
    department = department.upper()
    title = unquote(title)
    course = Course.objects.get(department=department, number=number, title=title, hours=hours)
    sections = Section.objects.all().filter(course=course)
    table = SectionTable(sections, exclude=['id', 'course'])
    RequestConfig(request).configure(table)
    return render(request, 'course.html', {'course': course, 'table': table})

def course_instructor(request, department, number, title ,hours, instructor):
    department = department.upper()
    title = unquote(title)
    instructor = unquote(instructor)
    course = Course.objects.get(department=department, number=number, title=title, hours=hours)
    sections = Section.objects.all().filter(course=course, instructor=instructor)
    table = SectionTable(sections, exclude=['id', 'course', 'instructor'])
    RequestConfig(request).configure(table)
    return render(request, 'course_instructor.html', {'course': course, 'instructor': instructor, 'table': table})
