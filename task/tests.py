from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from projects.models import Project
from task.models import Task

User = get_user_model()


class TaskAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="test123"
        )

        # authenticate user
        self.client.force_authenticate(user=self.user)

    def test_get_tasks_list(self):
        url = reverse("task-list")  # router name
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)





class TaskCreateAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="creator",
            email="creator@test.com",
            password="test123"
        )

        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(
            project_name="Test Project",
            description="Test desc",
            project_owner=self.user
        )

    def test_create_task(self):
        url = reverse("task-list")

        payload = {
            "title": "Test Task",
            "description": "Test Description",
            "project": self.project.id,
            "status": "todo",
            "priority": "MEDIUM",
            "due_date": "2025-12-31"
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

class TaskPermissionTest(APITestCase):

    def test_unauthenticated_user_cannot_create_task(self):
        url = reverse("task-list")

        payload = {
            "title": "Blocked Task",
            "description": "Should not work"
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
