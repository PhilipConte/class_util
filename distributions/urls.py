from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.table, name='table'),
    path('course/<str:department>+<int:number>', views.course_shortcut, name='course_shortcut'),
    path('course/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>', views.course, name='course'),
    path('course/department=<str:department>+number=<int:number>+title=<str:title>+hours=<int:hours>/<str:instructor>', views.course_instructor, name='course_instructor'),
]
