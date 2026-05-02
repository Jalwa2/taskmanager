
"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views_frontend
from core.views_frontend import logout_view

# 🌐 Simple homepage (optional)
def home(request):
    return HttpResponse("Team Task Manager API is running ")


urlpatterns = [
    # 🏠 UI PAGES
    path('', views_frontend.login_page),
    path('dashboard/', views_frontend.dashboard),
    path('projects-ui/', views_frontend.projects_page),
    path('tasks-ui/', views_frontend.tasks_page),
    path('logout/', logout_view),
    path('signup/', views_frontend.signup_page), # 🛠 Admin
    path('admin/', admin.site.urls),

    # 📦 APIs
    path('api/', include('core.urls')),

    # 🔐 JWT
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
