# 1️⃣ IMPORTS (TOP)
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


# 2️⃣ CUSTOM PERMISSION CLASS
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow only admin users to create/update/delete.
    Other authenticated users can view.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.role == 'admin'


# 3️⃣ PROJECT API
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


# 4️⃣ TASK API
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]


# 5️⃣ TASK STATISTICS API
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def task_statistics(request):
    """
    Returns task statistics:
    - total_tasks: Total number of tasks
    - completed_tasks: Tasks with status 'done'
    - pending_tasks: Tasks with status 'pending'
    - overdue_tasks: Tasks with deadline in the past and not completed
    """
    today = timezone.now().date()
    
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='done').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    overdue_tasks = Task.objects.filter(
        deadline__lt=today
    ).exclude(status='done').count()
    
    return Response({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
    }, status=status.HTTP_200_OK)