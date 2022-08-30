from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

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
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe_images/',
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        'AmountIngredient',
        blank=True, 
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
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

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='Recipe_amount',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        blank=True,  # null=True,
        related_name='amount_ingredient'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return f'{self.amount} {self.ingredient.measurement_unit} {self.ingredient.name}'

class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorite')
        ]

    def __str__(self):

        return f'{self.recipe} {self.user}'