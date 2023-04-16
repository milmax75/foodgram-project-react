import base64  # Модуль с функциями кодирования и декодирования base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from recipes.models import (
    Recipe,
    Ingredients,
    Tag,
    ShopList,
    Favourites,
    Follow,
)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):

    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'cooktime', 'ingredient', 'tag',
                  'author', 'quantity', 'is_favorited', 'is_in_shopping_cart')

    '''def get_is_favorited(self, obj):
        if 
        return dt.datetime.now().year - obj.birth_year 
    
    def get_is_in_shopping_cart(self, obj):
        return dt.datetime.now().year - obj.birth_year '''


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'units')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopList
        fields = ('user', 'recipe')


class FavouritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        fields = ('user', 'recipe')
