from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from distributions.models import Section, Course
from distributions.filters import SectionFilter, CourseFilter
from .serializers import SectionSerializer, SectionInstructorSerializer, CourseSerializer
from .paginators import DistributionsLimitOffsetPaginator

class SectionListAPIView(ListAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    filterset_class = SectionFilter
    pagination_class = DistributionsLimitOffsetPaginator


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['department', 'number', 'title', 'hours']
    pagination_class = DistributionsLimitOffsetPaginator

class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'

class CourseInstructorDetailAPIView(ListAPIView):
    serializer_class = SectionInstructorSerializer
    pagination_class = DistributionsLimitOffsetPaginator

    def get_queryset(self):
        slug = self.kwargs['slug']
        instructor = self.kwargs['instructor']
        course = get_object_or_404(Course, slug=slug)
        return course.sections.filter(instructor=instructor)
