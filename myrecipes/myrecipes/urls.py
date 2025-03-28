"""
URL configuration for myrecipes project.

The `urlpatterns` list routes URLs to views. For more info: https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
- Function views: path('', views.home, name='home')
- Class-based views: path('', Home.as_view(), name='home')
- Including another URLconf: path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Добавлено для встроенных представлений входа/выхода

# Список маршрутов проекта
urlpatterns = [
    path("admin/", admin.site.urls),           # Маршрут для админ-панели
    path("", include("recipes.urls")),         # Подключение маршрутов приложения recipes
    # Используем встроенные представления для входа и выхода
    path("login/", auth_views.LoginView.as_view(template_name="recipes/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="recipe_list"), name="logout"),
]

# Обслуживание медиафайлов в режиме отладки (для разработки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Позволяет видеть изображения в DEBUG-режиме