from django.shortcuts import render
from django.http import HttpResponse
from .models import Section
from django_tables2 import RequestConfig
from .tables import SectionTable

def table(request):
    sections = Section.objects.all()
    table = SectionTable(sections)
    RequestConfig(request).configure(table)
    return render(request, 'table.html', {'table': table})

def course(request, department, number):
    department = department.upper()
    sections = Section.objects.all().filter(department=department, course_number=number)
    table = SectionTable(sections)
    RequestConfig(request).configure(table)
    return render(request, 'course.html', {'department': department, 'number': number, 'table': table})
