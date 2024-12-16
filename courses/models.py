from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    semester = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True,unique=True, default='', editable=False)
    sks = models.PositiveIntegerField(default=2)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.id} - {self.name}"