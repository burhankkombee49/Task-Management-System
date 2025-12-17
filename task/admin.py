from django.contrib import admin
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from comment.models import Comment

# admin.site.register(Task)

class CommentInline(admin.TabularInline):
    
    model = Comment
    extra = 0  
    readonly_fields = ('created_at',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'assignee', 'created_by', 'due_date', 'comment_count')
    list_filter = ('status', 'priority', 'project')
    search_fields = ('title', 'assignee__username', 'created_by__username')
    inlines = [CommentInline]

    def comment_count(self, obj):
        return obj.comments.count()

    comment_count.short_description = 'Total Comments'

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)