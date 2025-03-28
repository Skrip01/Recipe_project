from django.urls import path
from . import views

# Маршруты приложения "recipes"
urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),                    # Главная страница со списком рецептов
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),  # Детали рецепта
    path("add/", views.add_recipe, name="add_recipe"),                  # Добавление рецепта
    path("recipe/<int:recipe_id>/edit/", views.edit_recipe, name="edit_recipe"),  # Редактирование рецепта
    path("recipe/<int:recipe_id>/delete/", views.delete_recipe, name="delete_recipe"),  # Удаление рецепта
    path("register/", views.register, name="register"),                 # Регистрация пользователя
    # Вход и выход перенесены в проектный urls.py
    path("recipe/<int:recipe_id>/like/", views.toggle_like, name="toggle_like"),  # Переключение лайка
    path("profile/", views.profile, name="profile"),                    # Страница профиля
    path("recipe/<int:recipe_id>/rate/", views.rate_recipe, name="rate_recipe"),  # Оценка рецепта
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),  # Удаление комментария
]