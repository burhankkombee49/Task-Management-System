# from django.test import TestCase
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# #!task/tests.py
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth.models import User
# from .models import Task
# from projects.models import Project_main

# class TaskAPITests(APITestCase):
    
#     # setUp runs ONCE before every test function. 
#     # It prepares a clean "stage".
#     def setUp(self):
#         # 1. We create a Boss (to give orders)
#         self.boss_user = User.objects.create_user(username='boss', password='password123')
#         # 2. We create an Employee (to take orders)
#         self.employee_user = User.objects.create_user(username='employee', password='password123')
        
#         # 3. We assume the Boss is logged in right now
#         self.client.force_authenticate(user=self.boss_user)

#         # 4. We need a project because a Task cannot exist without one
#         self.project = Project_main.objects.create(
#             project_name="Alpha Project",
#             description="Test Desc",
#             project_owner=self.boss_user
#         )

#         # 5. This gets the URL for "/api/tasks/" automatically
#         self.list_url = reverse('task-list')

#     # TEST 1: Can we create a task?
#     def test_create_task(self):
#         data = {
#             "title": "Fix Server",
#             "description": "Urgent fix",
#             "project": self.project.id,
#             "priority": "HIGH",
#             "status": "todo",
#             "due_date": "2025-12-31T12:00:00Z"
#         }
        
#         # We send a POST request (like a form submission)
#         response = self.client.post(self.list_url, data)
        
#         # We expect a "201 Created" success stamp
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
#         # We check the database: Is there exactly 1 task now?
#         self.assertEqual(Task.objects.count(), 1)

#     # TEST 2: Does the "My Tasks" filter work?
#     def test_filter_my_tasks(self):
#         # Boss creates a task for the Employee
#         Task.objects.create(
#             title="Task for Employee",
#             description="Do this",
#             project=self.project,
#             created_by=self.boss_user,
#             assignee=self.employee_user, # <--- Assignee is Employee
#             due_date="2025-12-31T12:00:00Z"
#         )

#         # Boss creates a task for Himself
#         Task.objects.create(
#             title="Task for Boss",
#             description="Do this",
#             project=self.project,
#             created_by=self.boss_user,
#             assignee=self.boss_user, 
#             due_date="2025-12-31T12:00:00Z"
#         )

#         # NOW: We switch login. The "Employee" is now using the app.
#         self.client.force_authenticate(user=self.employee_user)
        
#         # Employee asks: "Show me my tasks"
#         url = reverse('task-mytasks') # URL: /api/tasks/my-tasks/
#         response = self.client.get(url)
        
#         # Result: Should only find 1 task (The one assigned to Employee)
#         # It should NOT see the Boss's task.
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['title'], "Task for Employee")

#     # TEST 3: Can an employee delete a task? (Should fail)
#     def test_permission_delete_restriction(self):
#         # Boss creates a task
#         task = Task.objects.create(
#             title="Important Task",
#             project=self.project,
#             created_by=self.boss_user,
#             assignee=self.employee_user, # Given to employee
#             due_date="2025-12-31T12:00:00Z"
#         )

#         # Employee logs in
#         self.client.force_authenticate(user=self.employee_user)
        
#         # Employee tries to DELETE it
#         url = reverse('task-detail', args=[task.id])
#         response = self.client.delete(url)
        
#         # Result: 403 FORBIDDEN (You are not allowed!)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
