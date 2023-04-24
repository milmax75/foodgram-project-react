from django.contrib import admin
from .models import Tag, Recipe, Ingredients, IngredientInRecipe

# Register your models here.


admin.site.register(Ingredients)
admin.site.register(IngredientInRecipe)


@admin.register(Tag)
class TagsAdmin(admin.ModelAdmin):
    """Для администрирования тегов."""

    list_display = ("pk", "name", "slug", "color")
    list_editable = ("name", "slug", "color")


'''class TagInLine(admin.TabularInline):
    model = Recipe.tags.through
    #readonly_fields = ('tag', 'tag_name')
    extra = 2
    min_num = 1'''


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    readonly_fields = ('ingredient_id', 'id')
    extra = 2
    min_num = 1


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    """Для администрирования рецептов."""

    list_display = ('id', 'name', 'description', 'cooktime', 'author')
    list_editable = ('name', 'description', 'cooktime')
    search_fields = ('name',)
    inlines = [IngredientInLine]
