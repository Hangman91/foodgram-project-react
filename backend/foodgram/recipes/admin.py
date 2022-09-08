from django.contrib import admin

from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'id', 'get_favorite_count')
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags', )

    def get_favorite_count(self, obj):
        return obj.users_favorites.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    search_fields = ('name',)
    list_filter = ('name',)


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
