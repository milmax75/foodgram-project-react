
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import BooleanField, Exists, OuterRef, Sum, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import (
    Favourites,
    Ingredients,
    IngredientInRecipe,
    Recipe,
    ShopList,
    Tag,
)
from rest_framework import mixins, viewsets
from rest_framework.permissions import SAFE_METHODS

from .filters import RecipesFilter, IngredientsFilter
from .permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    IngredientsSerializer,
    RecipesReadSerializer,
    CreateUpdateRecipeSerializer,
    TagsSerializer,
)

User = get_user_model()

FILE_NAME = "shopping-list.txt"
TITLE_SHOP_LIST = "Список покупок с сайта Foodgram:\n\n"


class ListRetrieveViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    permission_classes = (IsAdminOrReadOnly,)


class TagViewSet(ListRetrieveViewSet):
    '''Вьюсет для списка тегов. Модель Tags.'''

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientsViewSet(ListRetrieveViewSet):
    '''Вьюсет для ингредиентов. Mодель Ingredients. '''

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [IngredientsFilter]
    search_fields = ['^name']


class RecipeViewSet(viewsets.ModelViewSet):
    '''Вьюсет для рецептов. Модель Recipes'''

    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_class = RecipesFilter

    def get_serializer_class(self):
        '''Сериализаторы рецептов.'''
        if self.request.method in SAFE_METHODS:
            return RecipesReadSerializer
        return CreateUpdateRecipeSerializer
