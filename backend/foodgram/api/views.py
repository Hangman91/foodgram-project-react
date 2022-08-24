from recipes.models import Tag, Recipe, Ingredient
from .mixins import ReadListOrObjectViewSet
from .serializers import TagSerializer, RecipeSerialiser, RecipePostSerialiser, IngredientSerialiser
from rest_framework import viewsets
from django.contrib.auth import get_user_model
User = get_user_model()

class TagViewSet(ReadListOrObjectViewSet):
    """Вьюсет для тэгов. Изменять тэги нельзя, потому рид онли"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""

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
