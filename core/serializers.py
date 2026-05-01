from rest_framework import serializers
from django.utils import timezone
from .models import User, Project, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        """Validate that deadline is not in the past"""
        if value < timezone.now().date():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

    def validate(self, data):
        """Validate that assigned user belongs to the project"""
        assigned_user = data.get('assigned_to')
        project = data.get('project')
        
        if assigned_user and project:
            if not project.members.filter(id=assigned_user.id).exists():
                raise serializers.ValidationError(
                    "Assigned user must be a member of the project."
                )
        
        return data