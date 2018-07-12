from django.contrib import admin
from . import models as m

@admin.register(m.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['term', 'course', 'CRN', 'instructor', 'average_GPA',
        'As', 'Bs', 'Cs', 'Ds', 'Fs', 'withdrawals', 'class_size']
