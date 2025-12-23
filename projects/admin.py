#!projects/admin.py
from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'project_name', 'project_owner', 'created_at')
    search_fields = ('project_name', 'project_owner__username')
    list_filter = ('created_at', 'project_owner')

admin.site.register(Project, ProjectAdmin)