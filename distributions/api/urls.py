from django.urls import include, path
from django.views.generic.base import RedirectView
from . import views

app_name = 'distributions-api'

urlpatterns = [
    path('sections/', views.SectionListAPIView.as_view(), name='section_list'),
    path('sections/<str:slug>/', views.SectionDetailAPIView.as_view(), name='section_detail'),
    path('courses/', views.CourseListAPIView.as_view(), name = 'course_list'),
    path('courses/<str:slug>/', views.CourseDetailAPIView.as_view(), name='course_detail'),
    path('courses/<str:slug>/<str:instructor>/', views.CourseInstructorDetailAPIView.as_view(), name='course_instructor_detail'),
]
