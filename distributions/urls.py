from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', RedirectView.as_view(url='courses/search/', permanent=False), name='index'),
    path('sections/', views.SectionFilteredListView.as_view(), name='section_filtered_list'),
    path('courses/home/', views.CourseListView.as_view(), name='course_list'),
    path('courses/search/', views.CourseSearchView.as_view(), name = 'course_search'),
    path('courses/', views.CourseFilteredListView.as_view(), name = 'course_filtered_list'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>/<str:instructor>/', views.CourseInstructorDetailView.as_view(), name='course_instructor_detail'),
]
