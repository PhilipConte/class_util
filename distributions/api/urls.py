from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

app_name = 'distributions-api'

urlpatterns = [
    path('sections/', views.SectionListAPIView.as_view(), name='section_list'),
    # path('courses/home/', views.CourseListView.as_view(), name='course_list'),
    # path('courses/search/', views.CourseSearchView.as_view(), name = 'course_search'),
    path('courses/', views.CourseListAPIView.as_view(), name = 'course_list'),
    path('courses/<int:pk>/', views.CourseDetailAPIView.as_view(), name='course_detail'),
    # path('courses/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>/<str:instructor>/', views.CourseInstructorDetailView.as_view(), name='course_instructor_detail'),
]
