from django.core.exceptions import ValidationError
from django_filters.fields import MultipleChoiceField
from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import BooleanWidget
from recipes.models import Recipe
from rest_framework.filters import SearchFilter


class IngredientsFilter(SearchFilter):
    '''Ingredients objects filter.'''
    search_param = 'name'


class TagsMultiChoiceField(MultipleChoiceField):
    '''Validation as field class for Tags Filter'''

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(
                self.error_messages['required'], code='required'
            )
        for v in value:
            if v in self.choices and not self.valid_value(v):
                raise ValidationError(
                    self.error_messages['invalid_choice'],
                    code='invalid_choice',
                    params={'value': v},
                )


class TagsFilter(filters.AllValuesMultipleFilter):
    '''Tags objects filter.'''

    field_class = TagsMultiChoiceField


class RecipesFilter(FilterSet):
    '''Recipes objects filter.'''

    tags = TagsFilter(field_name='tags__slug', label='Slug')
    author = filters.AllValuesMultipleFilter(
        field_name='author__id', label='Author'
    )
    is_in_shop_cart = filters.BooleanFilter(
        widget=BooleanWidget(), label='In shop cart'
    )
    is_in_favs = filters.BooleanFilter(
        widget=BooleanWidget(), label='In favorit'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_in_shop_cart', 'is_in_favs')
