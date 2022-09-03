import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Follow

from .filters import IngredientFilter, RecipeFilter
from .mixins import (ReadListObjectViewSet, ReadOrCreateViewSet)
from .permissions import AuthorOrReadOnly
from .serializers import (FavoriteSerializer, FollowListSerializer,
                          IngredientSerialiser, RecipePostSerialiser,
                          RecipeSerialiser, ShoppingCartSerializer,
                          TagSerializer)

User = get_user_model()


class TagViewSet(ReadListObjectViewSet):
    """Вьюсет для тэгов. Изменять тэги нельзя, потому рид онли"""

    permission_classes = (permissions.AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов"""
    permission_classes = (AuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

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

    @action(methods=('post', 'delete'), detail=False,
            url_path=r'(?P<pk>\d+)/shopping_cart',
            permission_classes=(permissions.IsAuthenticated,))
    def shopping_cart(self, request, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            shopping_cart_serializer = ShoppingCartSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            shopping_cart_serializer.is_valid(raise_exception=True)
            shopping_cart_serializer.save()
            return self.retrieve(request)
        elif request.method == 'DELETE':
            shopping_cart = get_object_or_404(
                ShoppingCart,
                user=user,
                recipe=recipe
            )
            shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('get',), detail=False,
            url_path='download_shopping_cart',
            url_name='download_shopping_cart',
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        recipes = user.shopping_list.values_list('recipe', flat=True)
        queryset = AmountIngredient.objects.filter(recipe__in=recipes).all()
        result = {}
        for ing_res in queryset:
            ing = ing_res.ingredient
            if ing.name not in result.keys():
                result[ing.name] = {
                    'name': ing.name,
                    'amount': ing_res.amount,
                    'unit': ing.measurement_unit
                }
            else:
                result[ing.name]['amount'] += ing_res.amount

        lines = ['Ингридиенты, Количество, ед. изм.\n']
        for line in result.values():
            lines.append('{name}, {amount}, {unit}\n'.format(**line))

        with open('Shopping_cart.txt', 'x') as shopping_list:
            shopping_list.writelines(lines)

        with open('Shopping_cart.txt', 'r') as shopping_list:
            response = HttpResponse(
                shopping_list,
                content_type='text/plain; charset="UTF-8"'
            )
            response['Content-Disposition'] = ('attachment;'
                                               'filename=Shopping_cart.txt')
        os.remove(os.path.abspath('Shopping_cart.txt'))
        return response


class IngredientViewSet(ReadListObjectViewSet):
    """Вьюсет для ингредиентов"""

    permission_classes = (permissions.AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialiser
    filterset_class = IngredientFilter


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

        return Response(status=status.HTTP_201_CREATED)

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
