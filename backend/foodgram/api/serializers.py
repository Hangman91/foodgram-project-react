from rest_framework import serializers
from users.models import User
from recipes.models import Tag, Recipe, Ingredient, AmountIngredient

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

class IngredientSerialiser(serializers.ModelSerializer):
    """Сериализатор для модели Ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')

class AmountIngredientSerialiser(serializers.ModelSerializer):
    """Сериализатор для модели Ингредиентов"""

    name = serializers.ReadOnlyField(source='ingredient.name')
    id = serializers.ReadOnlyField(source='ingredient.id')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name','measurement_unit','amount')
        read_only_fields = ('name',)



class RecipeSerialiser(serializers.ModelSerializer):
    """Сериализатор для модели Рецептов"""


    tags = TagSerializer(many=True)
    ingredients = AmountIngredientSerialiser(many=True)

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'ingredients', 'tags', 'cooking_time')
      #  read_only_fields = ('author',)

