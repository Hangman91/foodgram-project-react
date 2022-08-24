from django.contrib.auth import get_user_model
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets

from .mixins import ReadListOrObjectViewSet
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerialiser, RecipePostSerialiser,
                          RecipeSerialiser, TagSerializer)

User = get_user_model()

class TagViewSet(ReadListOrObjectViewSet):
    """Вьюсет для тэгов. Изменять тэги нельзя, потому рид онли"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeSerialiser
        elif self.request.method in ("POST", "PATCH"):
            return RecipePostSerialiser

    def perform_create(self, serializer):
        """Переназначаем create, чтобы подсунуть в него автора"""
        serializer.save(
            author=self.request.user
        )


class IngredientViewSet(ReadListOrObjectViewSet):
    """Вьюсет для ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialiser
