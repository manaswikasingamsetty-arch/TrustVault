
from django.db import models
from django.contrib.auth.models import User
import os


def document_upload_path(instance, filename):
    return f"user_documents/user_{instance.user.id}/{filename}"


class Document(models.Model):
    FILE_TYPES = [
        ("PDF", "PDF"),
        ("IMAGE", "Image"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    title = models.CharField(max_length=150)

    file = models.FileField(
        upload_to=document_upload_path
    )

    file_type = models.CharField(
        max_length=10,
        choices=FILE_TYPES
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
