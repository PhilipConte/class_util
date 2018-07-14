from .models import Course, Section
import django_filters

class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'department': ['icontains'],
            'number': ['contains'],
            'title': ['icontains'],
            'hours': ['exact'],
        }


class SectionFilter(django_filters.FilterSet):
    class Meta:
        model = Section
        fields = {
            'course__department': ['icontains'],
            'course__number': ['contains'],
            'course__title': ['icontains'],
            'course__hours': ['exact'],
            'instructor': ['icontains'],
            'CRN': ['contains'],
            'average_GPA': ['exact', 'lt', 'gt'],
            'term__semester': ['iexact'],
            'term__year': ['exact'],
        }
