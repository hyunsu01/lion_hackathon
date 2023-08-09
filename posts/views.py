# posts/views.py
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostModelSerialer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerialer

