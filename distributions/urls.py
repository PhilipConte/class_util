from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='courses', permanent=False), name='index'),
    path('sections', views.SectionSingleTableView.as_view(), name='sections'),
    path('sections/filterable', views.SectionFilteredSingleTableView.as_view(), name = 'sections_filterable'),
    path('courses', views.CourseSingleTableView.as_view(), name='courses'),
    path('courses/filterable', views.CourseFilteredSingleTableView.as_view(), name = 'courses_filterable'),
    path('courses/<str:department>+<int:number>', views.course_shortcut, name='course_shortcut'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>', views.course, name='course'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>/<str:instructor>', views.course_instructor, name='course_instructor'),
]
