from django.urls import path, include
from rest_framework.routers import DefaultRouter
from task.views import TaskViewSet, DashboardAPIView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),          # /api/tasks/...
    path('dashboard/', DashboardAPIView.as_view()),  # /api/dashboard/
]
    