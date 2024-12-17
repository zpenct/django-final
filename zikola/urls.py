from django.contrib import admin
from django.urls import include, path
from zikola import views

urlpatterns = [
    path("", views.index, name="main"),
    path('admin/', admin.site.urls),
    path('courses/', include('courses.urls', namespace="courses")),
    path('tasks/', include('tasks.urls', namespace="tasks")),
]
