from django.shortcuts import render

def login_page(request):
    return render(request, 'core/login.html')

def dashboard(request):
    return render(request, 'core/dashboard.html')

def projects_page(request):
    return render(request, 'core/projects.html')

def tasks_page(request):
    return render(request, 'core/tasks.html')