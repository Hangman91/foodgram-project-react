from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_list_or_404, get_object_or_404
from recipes.models import Favorite, Ingredient, Recipe, Tag
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Follow

from .mixins import (CreateOrDeleteViewSet, ReadListOrObjectViewSet,
                     ReadListViewSet, ReadOrCreateViewSet)
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, FollowListSerializer,
                          IngredientSerialiser, RecipePostSerialiser,
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

    @action(methods=('post', 'delete'), detail=False,
            url_path=r'(?P<pk>\d+)/favorite',
            permission_classes=(permissions.IsAuthenticated,))
    def favorite(self, request, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            favorite_serializer = FavoriteSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            favorite_serializer.is_valid(raise_exception=True)
            favorite_serializer.save()
            return self.retrieve(request)
        elif request.method == 'DELETE':
            favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(ReadListOrObjectViewSet):
    """Вьюсет для ингредиентов"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialiser

class FollowListViewSet(ReadOrCreateViewSet):

    serializer_class = FollowListSerializer

    def get_queryset(self):
        return get_list_or_404(User, following__user=self.request.user)

    def create(self, request, *args, **kwargs):

        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        double_subscribe = Follow.objects.filter(
            user=request.user,
            following=user
        ).exists()

        if request.user.id == int(user_id):
            error = {'errors': 'Невозможно подписаться на самого себя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        elif double_subscribe:
            error = {'errors': 'Вы уже подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(
            user=request.user, following=user)

        return Response(status=status.HTTP_201_CREATED )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs['users_id']
        subscribe_user = get_object_or_404(User, id=user_id)

        try:
            subscribe = Follow.objects.get(
                user=request.user,
                following=subscribe_user
            )
        except ObjectDoesNotExist:
            error = {'errors': 'Вы не подписаны на этого пользователя'}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    