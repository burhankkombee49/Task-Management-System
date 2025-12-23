from django.shortcuts import render
from django.http import HttpResponse
import datetime
from rest_framework import serializers
from .models import Comment
from .serializers import CommentSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets


# Create your views here.

class CommentViewSet(viewsets.ModelViewSet):
        queryset = Comment.objects.all()
        serializer_class = CommentSerializer
        permission_classes = [IsAuthenticated]

        def perform_create(self , serializer):
                serializer.save(author =self.request.user)

       


        


        


    # @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    # def add_comment(self, request, pk=None):
    #     task = self.get_object()

    #     serializer = CommentSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(
    #             task=task,
    #             author=request.user
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    # def comments(self, request, pk=None):
    #     task = self.get_object()
    #     comments = task.comments.all()
    #     serializer = CommentSerializer(comments, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
