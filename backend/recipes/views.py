from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Ingredients, Recipe, Tag, ShopList, Favourites
from .serializers import (
    IngredientsSerializer,
    TagSerializer,
    FavouritesSerializer,
    ShopListSerializer
)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IngredientsFilter

#from .permissions import AllowAny


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [IngredientsFilter]
    search_fields = ['^name']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavouritesViewSet(viewsets.ModelViewSet):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesSerializer


class ShopListViewSet(viewsets.ModelViewSet):
    queryset = ShopList.objects.all()
    serializer_class = ShopListSerializer
