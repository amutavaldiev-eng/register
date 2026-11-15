from django.db import models
from datetime import datetime 
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=530)
    caption = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)
    
    
    def __str__(self):
        return self.title