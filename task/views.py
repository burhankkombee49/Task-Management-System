from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from .models import Task
from .serializers import TaskSerializer
from .permission import IsTaskCreatorOrAssignee


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'due_date', 'assignee']
    search_fields = ['title', 'description', 'priority', 'status']

    permission_classes = [
        permissions.IsAuthenticated,
        IsTaskCreatorOrAssignee,
    ]

    def perform_create(self, serializer):
        task = serializer.save(created_by=self.request.user)


        if task.assignee and task.assignee.email:
            self.send_task_assignment_email(task)

    def send_task_assignment_email(self, task):
        subject = "You have been assigned a new task"
        message = (
            f"Hello {task.assignee.username},\n\n"
            f"You have been assigned a new task.\n\n"
            f"Task: {task.title}\n"
            f"Project: {task.project.project_name}\n"
            f"Assigned by: {task.created_by.username}\n\n"
            f"Please check the system for more details."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[task.assignee.email],
            fail_silently=True,
        )

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-tasks')
    def mytasks(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)


class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_tasks = Task.objects.filter(assignee=user)

        return Response({
            "statistics": {
                "total": user_tasks.count(),
                "todo": user_tasks.filter(status='todo').count(),
                "in_progress": user_tasks.filter(status='inprogress').count(),
                "done": user_tasks.filter(status='done').count(),
            }
        })
