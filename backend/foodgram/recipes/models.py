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
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        upload_to='recipe_images/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        'AmountIngredient',
        blank=True,
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='recipes',
        verbose_name='Тэг'
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время готовки'
    )

    class Meta:
        ordering = ('id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тэга'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):

    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Мера измерения'
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

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
        related_name='amount_ingredient',
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        ordering = ('recipe', )
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количества ингредиентов'

    def __str__(self):
        return (
            f'{self.amount}',
            f'{self.ingredient.measurement_unit}',
            f'{self.ingredient.name}'
        )


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='users_favorites',
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


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_list',
        help_text='Владелец списка покупок'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в списке покупок',
        on_delete=models.CASCADE,
        related_name='users_carts',
        help_text='Корзины пользователей'
    )

    class Meta:
        ordering = ('recipe', )
        verbose_name = 'Элемент списка покупок'
        verbose_name_plural = 'Элементы списка покупок'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_cart_item'
            ),
        )

    def __str__(self) -> str:
        return f'{self.recipe} in cart {self.user}'
