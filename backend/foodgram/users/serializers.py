from rest_framework import serializers

from users.models import User, Follow
from recipes.models import Recipe


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'id'
        )

    def get_is_subscribed(self, obj):

        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Follow.objects.filter(
            user=request.user,
            following__id=obj.id
        ).exists():
            return True
        return False


class FollowListSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Follow"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'recipes',
            'recipes_count',
            'is_subscribed'
        )
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name'
        )

    def get_is_subscribed(self, obj):

        request = self.context.get('request')
        if request.user.is_anonymous:
            return False
        if Follow.objects.filter(
            user=request.user, following__id=obj.id
        ).exists():
            return True
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.method == 'GET':
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        else:
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return RecipeMinifieldSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        request = self.context.get('request')
        if request.method == 'GET':
            queryset = Recipe.objects.filter(author__id=obj.id).order_by('id')
        return queryset.count()


class RecipeMinifieldSerializer(serializers.ModelSerializer):
    """Сериализатор для показа небольшого количества информации о рецепте"""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'cooking_time',
            'image'
        )
