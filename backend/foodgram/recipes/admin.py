from django.contrib import admin

from .models import AmountIngredient, Ingredient, Recipe, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'author', 'id')
    search_fields = ('name',)
    list_filter = ('tags',)


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


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(AmountIngredient, AmountIngredientAdmin)
