from django.db import models

# Create your models here.
"""
models.py - Defines Django models for the application.

This module contains the definition of Django models representing different entities
in the application, including users, tokens, products, reviews, orders, etc.
"""
import uuid
from django.db import models
from django.utils import timezone

# Create your models here.


class BaseModel(models.Model):
    """
    An abstract base model with common fields for other models.
    """

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, max_length=255
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        """
        Configuration options for the model.

        This model is abstract and not meant to be instantiated directly.
        """

        # pylint: disable=too-few-public-methods
        abstract = True


class User(BaseModel):
    fname = models.CharField(max_length=255, default="")
    lname = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255, default="", unique=True)
    password = models.TextField(default="")
    otp = models.IntegerField(default=0)
    otp_count = models.IntegerField(default=0)
    otp_status = models.BooleanField(default=False)
    no_of_attempts_allowed = models.IntegerField(default=3)
    no_of_wrong_attempts = models.IntegerField(default=0)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.email}"


class UserToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)



class Project(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    contributor_users = models.ManyToManyField(User, related_name='projects')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Task(BaseModel):
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50)
    due_date = models.DateField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title