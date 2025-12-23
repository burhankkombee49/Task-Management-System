
from rest_framework import viewsets , permissions
from . models import  Project
from . serializers import ProjectSerializer
from . permissions import  IsProjectOwner
from django.db.models import Q


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Project.objects.filter(
            Q(project_owner=user) |
            Q(tasks__assignee=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(project_owner=self.request.user)
