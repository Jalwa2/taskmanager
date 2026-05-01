from django.contrib.auth.models import AbstractUser
from django.db import models


# 👤 1. USER MODEL (FIRST)
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')


# 📁 2. PROJECT MODEL (JUST BELOW USER)
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_projects")
    members = models.ManyToManyField(User, related_name="projects")

    def __str__(self):
        return self.name


# ✅ 3. TASK MODEL (BELOW PROJECT)
class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateField()

    def __str__(self):
        return self.title