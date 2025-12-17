from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Project_main(models.Model):
    project_name = models.CharField(max_length=100)
    project_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project_name
