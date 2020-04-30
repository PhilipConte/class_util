from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from distributions.models import Section, Course, Pathway
from distributions.filters import CourseFilter, CourseFilterMulti, GroupedSectionFilter
from .serializers import CourseSerializer, SectionSerializer, GroupedSectionSerializer, PathwaySerializer


class PathwaysAPIView(ListAPIView):
    queryset = Pathway.objects.all()
    serializer_class = PathwaySerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_class = CourseFilter


class CourseSearchListAPIView(CourseListAPIView):
    filterset_class = CourseFilterMulti


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = 'slug'


class CourseInstructorsListAPIView(ListAPIView):
    serializer_class = GroupedSectionSerializer
    filterset_class = GroupedSectionFilter

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        return course.sections.group_by_instructor()


class CourseInstructorDetailAPIView(ListAPIView):
    serializer_class = SectionSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, slug=self.kwargs['slug'])
        return course.sections.filter(instructor=self.kwargs['instructor'])


class _SectionsRetrieveAPIView(RetrieveAPIView):
    def get_queryset(self, **kwargs):
        course = get_object_or_404(Course, slug=kwargs.get('slug'))
        if kwargs.get('instructor'):
            return course.sections.filter(instructor=kwargs.get('instructor'))
        return course.sections.all()


class StatsAPIView(_SectionsRetrieveAPIView):
    def get(self, request, **kwargs):
        data = self.get_queryset(**kwargs).stats()
        average_GPA = data.pop('average_GPA')
        data.pop('students')
        data.pop('withdrawals')

        return Response({
            'labels': data.keys(),
            'data': data.values(),
            'average_GPA': average_GPA,
            'chartType': 'doughnut',
        })


class HistoryAPIView(_SectionsRetrieveAPIView):    
    def get(self, request, **kwargs):
        sections = self.get_queryset(**kwargs)
        data = sections.group_by_term()

        return Response({
            'labels': [str(key) for key in data.keys()],
            'data': data.values(),
            'average_GPA': sections.stats()['average_GPA'],
            'chartType': 'bar',
        })
