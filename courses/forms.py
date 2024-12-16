from django import forms
from . import models

class CourseForm(forms.ModelForm):    
    class Meta:
        model = models.Course
        fields = ['name', 'semester', 'description','sks']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Basis Data'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control',
                                                  'placeholder': '1',
                                                  'min':1,
                                                  'max':8}),
            'sks': forms.NumberInput(attrs={'class': 'form-control',
                                                  'placeholder': '2',
                                                  'min':1,
                                                  'max':8}),
        }
