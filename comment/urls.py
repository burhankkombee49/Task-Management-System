from django.urls import path 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet


router = DefaultRouter()
router.register(r'comments', CommentViewSet)
urlpatterns = router.urls