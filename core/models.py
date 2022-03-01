from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    text = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
