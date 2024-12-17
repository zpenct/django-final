from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path("", views.TaskListView.as_view(), name="tasks_list"),
    path("new/", views.TaskCreateView.as_view(), name="task_new"),
    path('<int:task_id>/update_status/', views.update_status, name='update_task_status'),
    path("<int:course_id>/new/", views.TaskCreateView2.as_view(), name="task_new_for_course"),
    path("<str:tasks_id>/", views.TaskDetailView.as_view(), name="tasks_detail"),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_edit"),
    path("status/<str:status>/", views.TaskListView.as_view(), name="tasks_by_status"),
    path('<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]