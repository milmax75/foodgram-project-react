import base64  # Модуль с функциями кодирования и декодирования base64
from django.db import models
from django.core.files.base import ContentFile
from rest_framework import serializers
# from rest_framework.generics import get_object_or_404
from recipes.models import (
    Recipe,
    Ingredients,
    Tag,
    ShopList,
    Favourites,
    IngredientInRecipe
)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'units')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredients.objects.all()
    )
    quantity = serializers.IntegerField(write_only=True, min_value=1)

    class Meta:
        model = IngredientInRecipe
        fields = ('quantity', 'recipe', 'id')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class CreateUpdateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientInRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name',
                  'description', 'cooktime')

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "Добавьте хотя бы один ингредиент."
            )
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        create_ingredients = [
            IngredientInRecipe(
                quantity=ingredient['quantity'],
                ingredient_id=ingredient['id'],
                recipe=recipe
            )
            for ingredient in ingredients
        ]
        IngredientInRecipe.objects.bulk_create(
            create_ingredients
        )
        return recipe


class RecipeSerializer(serializers.ModelSerializer):

    image = Base64ImageField(required=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'cooktime', 'ingredient', 'tag',
                  'author', 'quantity', 'is_favorited', 'is_in_shopping_cart')

    '''def get_is_favorited(self, obj):
        if 
        return dt.datetime.now().year - obj.birth_year 
    
    def get_is_in_shopping_cart(self, obj):
        return dt.datetime.now().year - obj.birth_year '''


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopList
        fields = ('user', 'recipe')


class FavouritesSerializer(serializers.ModelSerializer):

    name = serializers.StringRelatedField(read_only=True)
    image = serializers.StringRelatedField(read_only=True)
    cooking_time = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Favourites
        fields = ('recipe', 'name', 'image', 'cooking_time')
