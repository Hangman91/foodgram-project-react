from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.models import AmountIngredient, Ingredient, Recipe, Tag
from rest_framework import serializers
from users.models import User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserMeSerializer(serializers.ModelSerializer):
    """Сериализатор для понимания, кто есть я."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'id')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тэгов"""

    class Meta:
        model = Tag
        fields = ('name', 'slug', 'color', 'id')


class TagCreateRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тэгов"""

    class Meta:
        model = Tag
        fields = ('id',)


class IngredientSerialiser(serializers.ModelSerializer):
    """Сериализатор для модели Ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerialiser(serializers.ModelSerializer):
    """Сериализатор для модели Ингредиентов"""

    name = serializers.ReadOnlyField(source='ingredient.name')
    id = serializers.ReadOnlyField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('name',)


class AmountIngrediensPostSerialiser(serializers.ModelSerializer):
   
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')
        read_only_fields = ('id',)

class RecipeSerialiser(serializers.ModelSerializer):
    """Сериализатор для показа модели  Рецептов"""

    tags = TagSerializer(many=True)
    ingredients = AmountIngredientSerialiser(many=True)
    author = UserMeSerializer()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'name', 'text',
            'ingredients',
            'tags',
            'cooking_time'
        )
        read_only_fields = ('author',)


class RecipePostSerialiser(serializers.ModelSerializer):
    """Сериализатор для создания  Рецептов"""

    ingredients = AmountIngrediensPostSerialiser(many=True)
    tags = serializers.ListField(
        child=serializers.SlugRelatedField(
            slug_field='id', queryset= Tag.objects.all()
        )
    )
    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name', 'text', 'cooking_time')
    
    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        new_ingredients = [
            AmountIngredient(
                ingredient=ingredient_data['id'],
                recipe=recipe,
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients_data
        ]
        obj = AmountIngredient.objects.bulk_create(new_ingredients)
        print(555,obj)
        recipe.ingredients.set(obj)
        return recipe

    def update(self, instance, validated_data):

        name = validated_data.pop('name')
        instance.name = name
        ingredients_data = validated_data.pop('ingredients')
        instance.ingredients.clear()
        new_ingredients = [
            AmountIngredient(
                ingredient=ingredient_data['id'],
                recipe=instance,
                amount=ingredient_data['amount']
            )
            for ingredient_data in ingredients_data
        ]
        obj = AmountIngredient.objects.bulk_create(new_ingredients)
        instance.ingredients.set(obj)

        return super().update(instance, validated_data)


    def to_representation(self, instance):
        return RecipeSerialiser(
            instance,
            context={
                'request': self.context.get('request')
            }).data