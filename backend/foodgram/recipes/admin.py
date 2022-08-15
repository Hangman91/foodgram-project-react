from django.contrib import admin

from .models import Recipe, Ingredient, Tag


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'author', 'tags') 
    search_fields = ('name',) 
    list_filter = ('tags',) 

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit') 
    search_fields = ('name',) 
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') 
    search_fields = ('name',) 
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin) 
admin.site.register(Ingredient, IngredientAdmin) 
admin.site.register(Tag, TagAdmin) 