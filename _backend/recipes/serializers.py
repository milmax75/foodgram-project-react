import base64  # Модуль с функциями кодирования и декодирования base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from recipes.models import (
    Recipe,
    Ingredients,
    Tag,
    Shoplist,
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

    class Meta:
        model = Recipe
        fields = '__all__'
        # read_only_fields = ('owner',)
