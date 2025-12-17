from django.urls import path 
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'projects', views.Project_mainViewSet, basename='projects') 

urlpatterns = router.urls
