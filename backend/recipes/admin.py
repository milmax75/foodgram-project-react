from django.contrib import admin
from .models import Tag, Recipe, Ingredients, IngredientInRecipe, Favourites


admin.site.register(Ingredients)
admin.site.register(IngredientInRecipe)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    '''Tags administration'''

    list_display = ('pk', 'name', 'slug', 'color')
    list_editable = ('name', 'slug', 'color')


class IngredientInLine(admin.TabularInline):
    '''Ability to manage ingredients in recipe'''
    model = IngredientInRecipe
    readonly_fields = ('id', )
    extra = 1
    min_num = 3


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    '''Recipes administration'''

    list_display = ('id', 'name', 'text', 'cooking_time', 'author', 'image')
    list_editable = ('name', 'text', 'cooking_time')
    search_fields = ('name',)
    inlines = [IngredientInLine]


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    '''Favourites administration'''

    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')
