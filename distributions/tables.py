import django_tables2 as tables
from .models import Section

class SectionTable(tables.Table):
    class Meta:
        model = Section
        template_name = 'django_tables2/bootstrap.html'
        exclude= 'id'
