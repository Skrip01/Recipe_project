from fileinput import filename

from django.db import models
from django.contrib.auth.models import User

# Модель категории рецептов
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Название категории, уникальное

    def __str__(self):
        return self.name  # Отображение названия в админке и формах

# Модель рецепта
class Recipe(models.Model):
    title = models.CharField(max_length=200)                   # Название рецепта
    description = models.TextField()                            # Описание рецепта
    ingredients = models.TextField(blank=True, verbose_name="Ингредиенты")
    steps = models.TextField()                                # Шаги приготовления
    cooking_time = models.PositiveIntegerField(help_text="Время в минутах")  # Время готовки
    image = models.ImageField(upload_to="recipe_images/", blank=True, null=True)  # Изображение (опционально)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор рецепта (удаляется при удалении пользователя)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Категория (может быть пустой)
    likes = models.ManyToManyField(User, related_name="liked_recipes", blank=True)  # Лайки от пользователей
    created_at = models.DateTimeField(auto_now_add=True)      # Дата создания (автоматически)

    def __str__(self):
        return self.title  # Отображение названия рецепта

# Модель комментария
class Comment(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name="comments")  # Связь с рецептом
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор комментария
    text = models.TextField("Комментарий", max_length=1000)    # Текст комментария с ограничением длины
    created_at = models.DateTimeField(auto_now_add=True)       # Дата создания

    def __str__(self):
        return f"{self.author.username}: {self.text[:20]}"     # Отображение автора и первых 20 символов текста


# Модель рейтинга
class Rating(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name="ratings")  # Связь с рецептом
    user = models.ForeignKey(User, on_delete=models.CASCADE)   # Пользователь, поставивший оценку
    value = models.PositiveSmallIntegerField("Оценка", default=0)  # Значение рейтинга

    class Meta:
        unique_together = ("recipe", "user")  # Один пользователь — одна оценка для рецепта

    def __str__(self):
        return f"{self.recipe.title} - {self.user.username}: {self.value}"  # Отображение рейтинга