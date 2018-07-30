from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='courses/search', permanent=False), name='index'),
    path('sections', views.SectionListView.as_view(), name='sections'),
    path('sections/filterable', views.SectionFilteredListView.as_view(), name = 'sections_filterable'),
    path('courses', views.CourseListView.as_view(), name='courses'),
    path('courses/search', views.CourseSearchView.as_view(), name = 'courses_search'),
    path('courses/search_results', views.CourseMultiFilteredListView.as_view(), name = 'courses_search_results'),
    path('courses/filterable', views.CourseFilteredListView.as_view(), name = 'courses_filterable'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>', views.CourseDetailView.as_view(), name='course'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>/<str:instructor>', views.CourseInstructorDetailView.as_view(), name='course_instructor'),
]
