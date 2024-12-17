from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from . import models
from . import forms

def detail(request, slug):
    course = models.Course.objects.get(slug=slug)
    print(course)
    context = {
        'Title': course.name,
        'Content': course.description,
        'Course': course,
        'Slug': slug
    }
    return render(request, 'courses/detail.html', context)

def semester(request, semester):
    courses = models.Course.objects.filter(semester=semester)
    context = {
        'Title': 'Home',
        'Content': 'Matakuliah Semester ' + str(semester),
        'Courses': courses,
        'range' : range(1,8),
        'selected_semester' : semester
        
    }
    return render(request, 'courses/index.html', context)

def new(request):
    if request.method == 'POST':
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Course successfully created!'}, status=200)
        else:
            return JsonResponse({'error': 'Form submission failed.'}, status=400)
    else:
        form = forms.CourseForm()
    context = {
        'course_form': form,
    }
    
    return render(request, 'courses/new.html', context)

class CourseListView(ListView):
    model = models.Course
    context = {
        'Title': 'Home',
        'Content': 'Welcome to the homepage',
        'range' : range(1,8),
        
    }
    template_name = 'courses/index.html'
    
    context_object_name = 'Courses'
    
    def get_queryset(self):
        semester =self.kwargs.get('semester', None)
        if semester:
            return models.Course.objects.filter(semester=semester)
        return models.Course.objects.order_by('semester')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Title'] = 'Home' 
        context['Content'] = 'Welcome to the homepage' 
        context['range'] = range(1, 8) 
        context['selected_semester'] = self.kwargs.get('semester', None)
        return context
    
class CourseCreateView(CreateView):
    model = models.Course
    form_class = forms.CourseForm
    template_name = 'courses/new.html'
    success_url = reverse_lazy('courses:course_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_form'] = context.pop('form')
        return context

    def form_valid(self, form):
        self.object = form.save()
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Course successfully created!'}, status=200)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
             return JsonResponse({'error': 'Form submission failed.', 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
class CourseDetailView(DetailView):
    model = models.Course
    template_name = 'courses/detail.html'
    slug_field = 'slug'       
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        context['Course'] = course
        context['Slug'] = course.slug
        context['Tasks'] = course.tasks.all()
        return context

from django.views.generic.edit import UpdateView

class CourseUpdateView(UpdateView):
    model = models.Course
    form_class = forms.CourseForm
    template_name = 'courses/edit.html'
    success_url = reverse_lazy('courses:course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = context.pop('form')
        return context