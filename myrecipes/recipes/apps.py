from django.apps import AppConfig

# Конфигурация приложения "recipes"
class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Тип первичного ключа по умолчанию для моделей
    name = 'recipes'                                      # Имя приложения