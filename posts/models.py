# posts/models.py

from django.db import models

class Post(models.Model):
    lesson_title = models.TextField(max_length=300)
    site_url = models.TextField(max_length=300, null=True, blank=True)
    image = models.TextField()
    price = models.IntegerField()
    field = models.IntegerField()
    # 매핑 1-6 : 1 DJango 2 React 3 Spring 4 C언어 5 Python 6 Java
