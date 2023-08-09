# posts/serializers.py

from rest_framework.serializers import ModelSerializer
from .models import Post

class PostModelSerialer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
