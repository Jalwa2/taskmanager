from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, TaskViewSet, task_statistics

router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('task-statistics/', task_statistics, name='task-statistics'),
]