from .models import Project_main
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project_main
        fields = ['id','project_name','description','created_at','updated_at']






