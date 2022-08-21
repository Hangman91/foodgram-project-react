from recipes.models import Tag, Recipe
from .mixins import ReadListOrObjectViewSet
from .serializers import TagSerializer, RecipeSerialiser
from rest_framework import viewsets 



class TagViewSet(ReadListOrObjectViewSet):
    """Вьюсет для тэгов. Изменять тэги нельзя, потому рид онли"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #permission_classes = (permissions.AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialiser

    def perform_create(self, serializer):
        """Переназначаем create, чтобы подсунуть в него автора"""
        serializer.save(
            author=self.request.user
        )