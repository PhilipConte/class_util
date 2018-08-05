from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
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

class SectionDetailAPIView(RetrieveAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    lookup_field = 'slug'

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

class _SectionsRetrieveAPIView(RetrieveAPIView):
    def get_queryset(self, **kwargs):
        course = get_object_or_404(Course, slug=kwargs.get('slug'))
        if kwargs.get('instructor'):
            sections = course.sections.filter(instructor=kwargs.get('instructor'))
        else:
            sections = course.sections.all()
        
        return sections

class StatsAPIView(_SectionsRetrieveAPIView):    
    def get(self, request, **kwargs):
        data = self.get_queryset(**kwargs).stats()
        average_GPA = data.pop('average_GPA')
        students = data.pop('students')
        withdrawals = data.pop('withdrawals')

        keys, values = data.keys(), data.values()

        out_dict = dict()
        out_dict['labels'] = keys
        out_dict['data'] = values
        out_dict['average_GPA'] = average_GPA
        out_dict['chartType'] = 'doughnut'

        return Response(out_dict)

class HistoryAPIView(_SectionsRetrieveAPIView):    
    def get(self, request, **kwargs):
        sections = self.get_queryset(**kwargs)
        data = sections.group_by_term()

        
        keys, values = data.keys(), data.values()

        out_dict = dict()
        out_dict['labels'] = [str(key) for key in keys]
        out_dict['data'] = values
        out_dict['average_GPA'] = sections.stats()['average_GPA']
        out_dict['chartType'] = 'bar'

        return Response(out_dict)
