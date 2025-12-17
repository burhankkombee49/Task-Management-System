
from rest_framework import viewsets , permissions
from . models import Project_main
from . serializers import ProjectSerializer
from . permissions import  IsProjectOwner

class Project_mainViewSet(viewsets.ModelViewSet):
   
    queryset = Project_main.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectOwner]

    def perform_create(self , serializer):
        serializer.save(project_owner=self.request.user)


