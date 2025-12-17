from datetime import datetime
from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.id")

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "assignee",
            "status",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
            "created_by",
        ]
        read_only_fields = ["created_at", "updated_at", "created_by"]

    def validate_due_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
