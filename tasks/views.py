from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from . import models
from . import forms
from courses.models import Course
from django.utils import timezone
from django.utils.timezone import make_aware
from django.views.generic.edit import UpdateView

def index(request):
    return render(request, 'tasks/index.html')

class TaskListView(ListView):
    model = models.Task
    template_name = 'tasks/index.html'
    
    context_object_name = 'Tasks'
    
    ordering =['due_date']
    
    def get_queryset(self):
        status =self.kwargs.get('status', None)
        if status:
            return models.Task.objects.filter(status=status)
        return models.Task.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Title'] = 'My Tasks' 
        context['Content'] = 'Welcome to my task' 
        context['Status'] = ['completed','pending', 'in_progress']
        context['Selected_status'] =self.kwargs.get('status', None)
        return context

class TaskDetailView(DetailView):
    model = models.Task
    template_name = 'tasks/detail.html'

    def get_object(self):
        tasks_id = self.kwargs.get("tasks_id")
        return get_object_or_404(models.Task, id=tasks_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()

        due_date = task.due_date
        if due_date.tzinfo is None:
            due_date = make_aware(due_date)

        now = timezone.now()

        time_left = due_date - now
        print(time_left.total_seconds())

        if time_left.total_seconds() < 0:
            status_message = "Task is overdue"
            time_left = abs(time_left)
        else:
            status_message = "Time left"

        hours_left = time_left.days * 24 + time_left.seconds // 3600
        minutes_left = (time_left.seconds // 60) % 60

        if time_left.total_seconds() < 0:
            context['Time_left'] = f'{hours_left} hours {minutes_left} minutes overdue'
        else:
            context['Time_left'] = f'{hours_left} hours {minutes_left} minutes left'

        context['Status_message'] = status_message
        context['Task'] = task
        return context
        
class TaskCreateView(CreateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'tasks/new.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = context.pop('form')
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Task successfully created!'}, status=200)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({'error': 'Form submission failed.', 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
class TaskCreateView2(CreateView):
    model = models.Task    
    form_class = forms.TaskForm
    template_name = 'tasks/new.html'
    success_url = reverse_lazy('tasks:task_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_id = self.kwargs.get('course_id')
        context['task_form'] = context.pop('form')
        if course_id:
            context['course'] = get_object_or_404(Course, id=course_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        course_id = self.kwargs.get('course_id')
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            initial['course'] = course
        return initial


def update_status(request, task_id):
    if request.method == 'POST':
        print("ke klik")
        task = models.Task.objects.get(id=task_id)
        if task.status == 'pending':
            task.status = 'in_progress'
        elif task.status == 'in_progress':
            task.status = 'completed'
        else:
            return JsonResponse({'error': 'Task already completed'}, status=400)

        task.save()
        return JsonResponse({'status': task.status})
    return JsonResponse({'error': 'Invalid request'}, status=400)

class TaskUpdateView(UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'tasks/edit.html'  
    success_url = reverse_lazy('tasks:tasks_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = context.pop('form')
        context['Title'] = 'Edit Task'
        return context