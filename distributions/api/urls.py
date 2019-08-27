from django.urls import path
from . import views

app_name = 'distributions-api'

urlpatterns = [
    path('courses/', views.CourseListAPIView.as_view(), name = 'course_list'),
    path('courses/search/', views.CourseSearchListAPIView.as_view(), name = 'course_search'),
    path('courses/<str:slug>/', views.CourseDetailAPIView.as_view(), name='course_detail'),
    path('courses/<str:slug>/stats/', views.StatsAPIView.as_view(), name='course_stats'),
    path('courses/<str:slug>/history/', views.HistoryAPIView.as_view(), name='course_history'),
    path('courses/<str:slug>/instructors/', views.CourseInstructorsListAPIView.as_view(), name='course_instructors'),
    path('courses/<str:slug>/instructors/<str:instructor>/', views.CourseInstructorDetailAPIView.as_view(), name='course_instructor_detail'),
    path('courses/<str:slug>/instructors/<str:instructor>/stats/', views.StatsAPIView.as_view(), name='course_instructor_stats'),
    path('courses/<str:slug>/instructors/<str:instructor>/history/', views.HistoryAPIView.as_view(), name='course_instructor_history'),
]
