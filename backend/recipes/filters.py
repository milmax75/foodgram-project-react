
from django_filters import rest_framework as filters
from .models import Ingredients, Recipe
from rest_framework import filters


class IngredientsFilter(filters.SearchFilter):
    
    search_param = 'name'
