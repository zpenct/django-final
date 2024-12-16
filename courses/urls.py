from django.urls import path

from . import views

app_name = 'courses'

urlpatterns = [
    path("", views.CourseListView.as_view(), name="course_list"),
    # path("new", views.new, name="course_new"),
    path("new", views.CourseCreateView.as_view(), name="course_new"),
    path("semester/<int:semester>", views.CourseListView.as_view(), name="course_by_semester"),
    path("<slug:slug>", views.CourseDetailView.as_view(), name="course_detail"),
    # path("<slug:slug>", views.detail, name="course_detail"),
    
]