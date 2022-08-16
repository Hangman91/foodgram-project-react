from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator 
User = get_user_model()


class Recipe(models.Model):

    """Класс Recipe, то есть Рецепт.
    Содержит следующие поля:
    *Автор публикации (пользователь).
    *Название.
    *Картинка.
    *Текстовое описание.
    *Ингредиенты: продукты для приготовления блюда по рецепту. 
    Множественное поле, выбор из предустановленного списка,
    с указанием количества и единицы измерения.
    *Тег (можно установить несколько тегов на один рецепт,
    выбор из предустановленных).
    *Время приготовления в минутах"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )

    name = models.CharField(
        max_length=200
    )
    #image = pass
    text = models.TextField()
    ingredients = models.ManyToManyField(
        'Ingredient',
        #on_delete=models.SET_NULL,
        blank=True, #null=True,
        related_name='recipes'
    )
    tags = models.ForeignKey(
        'Tag',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='recipes'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    def __str__(self):
        return self.name

class Tag(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )
    color = models.CharField(
        max_length=7,
        unique=True
    )
    def __str__(self):
        return self.name

class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True
    )

    measurement_unit = models.CharField(
        max_length=200
    )

    amount = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    def __str__(self):
        return self.name