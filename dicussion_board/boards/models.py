from django.db import models

# import
from django.contrib.auth.models import User
from django.utils.text import Truncator


# Create your models here.


# ================================================================
class Board(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by("-created_dt").first()


class Topic(models.Model):
    subject = models.CharField(max_length=255, null=False)
    board = models.ForeignKey(Board, related_name="topics", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        User, related_name="topics", on_delete=models.CASCADE
    )
    created_dt = models.DateTimeField(auto_now_add=True)
    # views = models.ManyToManyField
    views = models.PositiveIntegerField(default=0)
    updated_by = models.ForeignKey(
        User, null=True, related_name="+", on_delete=models.CASCADE
    )
    updated_dt = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=5000, null=False)
    topic = models.ForeignKey(Topic, related_name="posts", on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, null=True, related_name="+", on_delete=models.CASCADE
    )
    updated_dt = models.DateTimeField(null=True)

    def __str__(self) -> str:
        truncted_message = Truncator(self.message)
        return truncted_message.chars(30)
