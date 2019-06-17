from django.urls import path
from django.views.generic.base import RedirectView
from . import views

app_name = 'distributions'

urlpatterns = [
    path('', RedirectView.as_view(url='courses/search/', permanent=False), name='index'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/search/', views.CourseSearchView.as_view(), name = 'course_search'),
    path('courses/filtered/', views.CourseFilteredListView.as_view(), name = 'course_filtered_list'),
    path('courses/<str:slug>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<str:slug>/instructor/<str:instructor>/', views.CourseInstructorDetailView.as_view(), name='course_instructor_detail'),
]
