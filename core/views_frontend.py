from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Project, Task

from django.contrib.auth import get_user_model
User = get_user_model()

# 🔐 LOGIN
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/dashboard/')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})

    return render(request, 'core/login.html')


# 📊 DASHBOARD
@login_required
def dashboard(request):

    today = timezone.now().date()

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='done').count()
    pending_tasks = Task.objects.filter(status='pending').count()
    overdue_tasks = Task.objects.filter(deadline__lt=today).exclude(status='done').count()

    return render(request, 'core/dashboard.html', {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks
    })


# 📁 PROJECTS
@login_required
def projects_page(request):

    if request.method == "POST":
        Project.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            created_by=request.user
        )

    projects = Project.objects.filter(created_by=request.user)

    return render(request, 'core/projects.html', {
        'projects': projects
    })


# ✅ TASKS
@login_required
def tasks_page(request):

    User = get_user_model()

    if request.method == "POST":
        Task.objects.create(
            title=request.POST.get("title"),
            status=request.POST.get("status"),
            project_id=request.POST.get("project"),
            assigned_to_id=request.POST.get("assigned_to"),
            deadline=timezone.now().date()
        )

    tasks = Task.objects.filter(assigned_to=request.user)
    projects = Project.objects.filter(created_by=request.user)
    users = User.objects.all()

    return render(request, 'core/tasks.html', {
        'tasks': tasks,
        'projects': projects,
        'users': users
    })

# 🚪 LOGOUT
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, 'core/signup.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(username=username, password=password)
        return redirect('/')

    return render(request, 'core/signup.html')