from django.db import models
from apps.users.models import User


class Password(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # delete todos when user is deleted
        related_name="todos",
    )
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # newest first by default

    def __str__(self):
        return self.name
