from django.contrib import admin
from .models import Section

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['term', 'year', 'department', 'course_number',
        'course_title', 'credit_hours', 'CRN', 'instructor', 'average_GPA',
        'As', 'Bs', 'Cs', 'Ds', 'Fs', 'withdrawals', 'class_size']
