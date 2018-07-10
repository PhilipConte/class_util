from django.shortcuts import render
from django.http import HttpResponse
from .models import Section

def table(request):
    sections = Section.objects.all()
    return render(request, 'table.html', {'sections': sections})

def course(request, department, number):
    department = department.upper()
    sections = Section.objects.all().filter(department=department, course_number=number)
    return render(request, 'course.html',
        {'department': department, 'number': number, 'sections': sections})
