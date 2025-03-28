"""
ASGI config for myrecipes project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

from django.contrib import admin
from .models import Recipe, Category

# Регистрация моделей в админ-панели для управления через интерфейс
admin.site.register(Recipe)   # Рецепты будут доступны в админке
admin.site.register(Category) # Категории тоже будут доступны
