from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  # Добавлено для сообщений об ошибках
from .models import Recipe, Category, Comment, Rating
from .forms import RecipeForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator  # Добавлено для пагинации
from django.db import models

# Главная страница со списком рецептов
def recipe_list(request):
    category_id = request.GET.get("category")  # Фильтр по категории из GET-запроса
    search_query = request.GET.get("search", "")  # Поисковый запрос
    recipes = Recipe.objects.all()  # Получаем все рецепты

    # Фильтрация по категории
    if category_id:
        try:
            recipes = recipes.filter(category_id=int(category_id))  # Безопасная проверка на число
        except ValueError:
            pass  # Игнорируем некорректный ID категории

    # Фильтрация по поисковому запросу (без учёта регистра)
    if search_query:
        recipes = recipes.filter(title__icontains=search_query)

    # Пагинация: 10 рецептов на страницу
    paginator = Paginator(recipes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()  # Все категории для фильтра
    return render(request, "recipes/index.html", {
        "page_obj": page_obj,  # Объект пагинации вместо списка рецептов
        "categories": categories,
        "search_query": search_query
    })

# Страница детального просмотра рецепта
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт или 404
    comments = recipe.comments.all().order_by("-created_at")  # Комментарии, новые сверху
    avg_rating = recipe.ratings.aggregate(models.Avg('value'))['value__avg'] or 0  # Средняя оценка или 0

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")  # Нужна авторизация для комментариев
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)  # Не сохраняем сразу
            comment.author = request.user  # Привязываем автора
            comment.recipe = recipe       # Привязываем рецепт
            comment.save()
            return redirect("recipe_detail", recipe_id=recipe.id)
        else:
            messages.error(request, "Ошибка в форме комментария.")  # Сообщение об ошибке
    else:
        comment_form = CommentForm()  # Пустая форма для GET-запроса

    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe,
        "comments": comments,
        "comment_form": comment_form,
        "avg_rating": avg_rating,
    })

# Добавление нового рецепта
@login_required  # Только для авторизованных пользователей
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)  # Форма с данными и файлами
        if form.is_valid():
            recipe = form.save(commit=False)  # Не сохраняем сразу
            recipe.author = request.user      # Привязываем текущего пользователя
            recipe.save()                     # Сохраняем рецепт
            return redirect("recipe_list")    # Переход на главную
        else:
            messages.error(request, "Ошибка в форме. Проверьте данные.")  # Сообщение об ошибке
    else:
        form = RecipeForm()  # Пустая форма для GET-запроса
    return render(request, "recipes/add_recipe.html", {"form": form})

# Регистрация нового пользователя
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # Форма регистрации
        if form.is_valid():
            user = form.save()  # Создаём пользователя
            login(request, user)  # Автоматический вход
            return redirect("recipe_list")
        else:
            messages.error(request, "Ошибка при регистрации.")  # Сообщение об ошибке
    else:
        form = UserCreationForm()
    return render(request, "recipes/register.html", {"form": form})

# Вход в систему (заменён встроенным LoginView в urls.py)
# def user_login(request):
#     Удалено, так как используется встроенное представление

# Выход из системы (заменён встроенным LogoutView в urls.py)
# def user_logout(request):
#     Удалено, так как используется встроенное представление

# Редактирование рецепта
@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт или 404
    if recipe.author != request.user:  # Проверка авторства
        return redirect("recipe_list")
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)  # Форма с текущими данными
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect("recipe_detail", recipe_id=recipe.id)
        else:
            messages.error(request, "Ошибка в форме. Проверьте данные.")  # Сообщение об ошибке
    else:
        form = RecipeForm(instance=recipe)  # Форма с данными рецепта
    return render(request, "recipes/edit_recipe.html", {"form": form, "recipe": recipe})

# Удаление рецепта
@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт или 404
    if recipe.author != request.user:  # Проверка авторства
        return redirect("recipe_list")
    if request.method == "POST":
        recipe.delete()  # Удаляем рецепт
        return redirect("recipe_list")
    return render(request, "recipes/delete_recipe.html", {"recipe": recipe})

# Страница профиля пользователя
@login_required
def profile(request):
    user_recipes = Recipe.objects.filter(author=request.user)  # Рецепты текущего пользователя
    return render(request, "recipes/profile.html", {"user_recipes": user_recipes})

# Переключение лайка
@login_required
def toggle_like(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт или 404
    if request.user in recipe.likes.all():
        recipe.likes.remove(request.user)  # Убираем лайк
    else:
        recipe.likes.add(request.user)     # Добавляем лайк
    # Возвращаемся на предыдущую страницу или на главную
    return redirect(request.META.get('HTTP_REFERER', 'recipe_list'))

# Оценка рецепта
@login_required
def rate_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт или 404
    if request.method == "POST":
        try:
            value = int(request.POST.get("value"))  # Получаем оценку
        except (TypeError, ValueError):
            messages.error(request, "Некорректная оценка.")  # Сообщение об ошибке
            return redirect("recipe_detail", recipe_id=recipe.id)
        if value < 1 or value > 5:  # Проверка диапазона
            messages.error(request, "Оценка должна быть от 1 до 5.")
            return redirect("recipe_detail", recipe_id=recipe.id)
        # Создаём или обновляем оценку
        rating, created = Rating.objects.get_or_create(recipe=recipe, user=request.user, defaults={'value': value})
        if not created:
            rating.value = value  # Обновляем значение
            rating.save()
    return redirect("recipe_detail", recipe_id=recipe.id)

# Удаление комментария
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Получаем комментарий или 404
    if comment.author != request.user:  # Проверка авторства
        return redirect("recipe_detail", recipe_id=comment.recipe.id)
    if request.method == "POST":
        recipe_id = comment.recipe.id  # Сохраняем ID рецепта
        comment.delete()              # Удаляем комментарий
        return redirect("recipe_detail", recipe_id=recipe_id)
    return render(request, "recipes/delete_comment.html", {"comment": comment})