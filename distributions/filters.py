from .models import Section
import django_filters

class SectionFilter(django_filters.FilterSet):
    class Meta:
        model = Section
        fields = {
            'course__department': ['icontains'],
            'course__title': ['icontains'],
        }
