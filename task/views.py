from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .permission import IsTaskCreatorOrAssignee
from comment.models import Comment
from comment.serializers import CommentSerializer



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
        serializer.save(created_by=self.request.user)


   #!tasks/views.py
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-tasks')
    def mytasks(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = self.get_serializer(tasks, many=True)
    
        return Response(serializer.data)


    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        task = self.get_object()

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                task=task,
                author=request.user
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        task = self.get_object()
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_tasks = Task.objects.filter(assignee=user)

        total_tasks = user_tasks.count()
        todo_count = user_tasks.filter(status='todo').count()
        progress_count = user_tasks.filter(status='inprogress').count()
        done_count = user_tasks.filter(status='done').count()

        return Response({
            "statistics": {
                "total": total_tasks,
                "todo": todo_count,
                "in_progress": progress_count,
                "done": done_count
            },
            
        })


        




       



