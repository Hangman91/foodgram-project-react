from django.contrib import admin

from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                     ShoppingCart, Tag)

# dfdsfsdfsd
from import_export import resources
from import_export.admin import ImportMixin


class IngResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        fields = ('measurement_unit', 'name',)

################################################




class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'author', 'id')
    search_fields = ('name',)
    list_filter = ('tags',)

class IngredientAdmin(ImportMixin, admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    search_fields = ('name',)
    list_filter = ('name',)
    resource_class = IngResource

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'id')
    search_fields = ('name',)
    list_filter = ('name',)


class AmountIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', 'id')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'id')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'id')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(AmountIngredient, AmountIngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
