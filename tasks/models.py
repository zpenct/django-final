from django.db import models

from courses import models as courses

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    
    course = models.ForeignKey(
        courses.Course,
        on_delete=models.CASCADE, 
        null=True,            
        blank=True,            
        related_name="tasks"  
    )
    
    def __str__(self):
        return self.title