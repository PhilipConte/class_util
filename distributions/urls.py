from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='courses/search', permanent=False), name='index'),
    path('sections', views.SectionSingleTableView.as_view(), name='sections'),
    path('sections/filterable', views.SectionFilteredSingleTableView.as_view(), name = 'sections_filterable'),
    path('courses', views.CourseSingleTableView.as_view(), name='courses'),
    path('courses/search', views.CourseSearch.as_view(), name = 'courses_search'),
    path('courses/search_results', views.CourseMultiFilteredSingleTableView.as_view(), name = 'courses_search_results'),
    path('courses/filterable', views.CourseFilteredSingleTableView.as_view(), name = 'courses_filterable'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>', views.course, name='course'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>/<str:instructor>', views.course_instructor, name='course_instructor'),
]
