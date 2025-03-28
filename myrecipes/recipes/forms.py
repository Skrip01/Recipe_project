from django import forms
from .models import Recipe, Category, Comment

# Форма для добавления и редактирования рецептов
class RecipeForm(forms.ModelForm):
    # Поле выбора категории (обязательное, без пустого значения по умолчанию)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, empty_label="Выберите категорию")

    class Meta:
        model = Recipe                        # Модель, с которой работает форма
        fields = ["title", "description", "ingredients", "steps", "cooking_time", "image", "category"]  # Поля формы

# Форма для добавления комментариев
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment                   # Модель комментария
        fields = ["text"]                 # Единственное поле — текст комментария
        widgets = {
            # Настройка виджета для текстового поля
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Введите ваш комментарий...'}),
        }