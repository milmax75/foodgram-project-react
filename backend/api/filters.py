from django.core.exceptions import ValidationError
from django_filters.fields import MultipleChoiceField
from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import BooleanWidget
from recipes.models import Recipe
from rest_framework.filters import SearchFilter


class IngredientsFilter(SearchFilter):
    '''Фильтр обьектов Ingredients.'''
    search_param = 'name'


class TagsMultipleChoiceField(MultipleChoiceField):
    '''Фильтр обьектов Tags.'''

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages['required'], code='required'
            )
        for val in value:
            if val in self.choices and not self.valid_value(val):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': val},
                )


class TagsFilter(filters.AllValuesMultipleFilter):
    '''Фильтр обьектов Tags.'''

    field_class = TagsMultipleChoiceField


class RecipesFilter(FilterSet):
    '''Фильтр обьектов Recipes.'''

    author = filters.AllValuesMultipleFilter(
        field_name='author__id', label='Author'
    )
    tags = TagsFilter(field_name='tags__slug')
    is_in_shopping_cart = filters.BooleanFilter(
        widget=BooleanWidget(), label='In shopping cart'
    )
    is_favorited = filters.BooleanFilter(
        widget=BooleanWidget(), label='In favourite'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited')
