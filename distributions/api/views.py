from rest_framework.generics import ListAPIView, RetrieveAPIView

from distributions.models import Section, Course
from distributions.filters import SectionFilter, CourseFilter
from .serializers import SectionSerializer, CourseSerializer

class SectionListAPIView(ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filterset_class = SectionFilter


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter

class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'
