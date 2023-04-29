from django.contrib import admin
from .models import Tag, Recipe, Ingredients, IngredientInRecipe


admin.site.register(Ingredients)
admin.site.register(IngredientInRecipe)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    """Для администрирования тегов."""

    list_display = ("pk", "name", "slug", "color")
    list_editable = ("name", "slug", "color")


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    readonly_fields = ('ingredient_id', 'id')
    extra = 2
    min_num = 1


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    """Для администрирования рецептов."""

    list_display = ('id', 'name', 'text', 'cooking_time', 'author')
    list_editable = ('name', 'text', 'cooking_time')
    search_fields = ('name',)
    inlines = [IngredientInLine]
