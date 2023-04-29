from django.db.models import BooleanField, Exists, OuterRef, Sum, Value
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
from django.http import HttpResponse
from users.models import Follow, UserCustomized
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from .filters import RecipesFilter, IngredientsFilter
from .permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from .serializers import (
    AddRecipeSerializer,
    IngredientsSerializer,
    GetRecipeSerializer,
    CreateUpdateRecipeSerializer,
    TagsSerializer,
    FollowSerializer,
    CheckFollowSerializer,
    CheckFavouriteSerializer,
    CheckShopCartSerializer
)
from core.pagination import StandardResultsSetPagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''Tags' viewset. Tags Model.'''

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    '''Recipes' viewset. Recipes Model.'''

    permission_classes = (IsAdminAuthorOrReadOnly,)
    filter_class = RecipesFilter

    def get_serializer_class(self):
        '''Recipes' serialization.'''
        if self.request.method in SAFE_METHODS:
            return GetRecipeSerializer
        return CreateUpdateRecipeSerializer

    def get_queryset(self):
        '''Check if recipe in shoplist and/or favs'''
        user = self.request.user
        if user.is_authenticated:
            return Recipe.objects.annotate(
                is_favorited=Exists(
                    user.fav_adder.filter(recipe__pk=OuterRef('pk'))),
                is_in_shopping_cart=Exists(
                    user.shopper.filter(recipe__pk=OuterRef('pk')))
            )
        return Recipe.objects.annotate(
            is_favorited=Value(False, output_field=BooleanField()),
            is_in_shopping_cart=Value(False, output_field=BooleanField()),
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=('POST', 'DELETE'),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        '''Add/Delete a recipe to/from the shoplist.'''
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = CheckShopCartSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            return self.add_object(ShopList, request.user, pk)
        return self.delete_object(ShopList, request.user, pk)

    def add_object(self, model, user, pk):
        '''Adding objects for favourites and shoplist.'''
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = AddRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_object(self, model, user, pk):
        '''Deleting objects from favourites and shoplist.'''
        model.objects.filter(user=user, recipe__id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('GET',), detail=False, permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        '''Download shoplist file in pdf format'''
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__shoplist_recipe__user=request.user
            )
            .select_related('ingredient').all()
            .prefetch_related('recipe').all()
            .values('ingredient__name', 'ingredient__measurement_unit')
            .order_by('ingredient__name')
            .annotate(total=Sum('amount'))
        )
        col1 = max(len(ingredient["ingredient__name"])
                   for ingredient in ingredients)
        col2 = max(len(str(ingredient["total"]))
                   for ingredient in ingredients)
        col3 = max(len(ingredient["ingredient__measurement_unit"])
                   for ingredient in ingredients)
        devider = (
            f'\n|{"_"*(col1+2)}|{"_"*(col2+2)}|{"_"*(col3+2)}|\n')
        output = 'The list of goods for your recipes. \n\n'
        output += f',{(len(devider)-devider.count("|"))*"_"},\n'
        output += devider.join(
            f'| {ingredient["ingredient__name"]} '
            f'{(col1-len(ingredient["ingredient__name"]))*" "}'
            f'| {ingredient["total"]}'
            f'{(col2-len(str(ingredient["total"])))*" "} '
            f'| {ingredient["ingredient__measurement_unit"]}'
            f'{(col3-len(ingredient["ingredient__measurement_unit"]))*" "} |'
            for ingredient in ingredients
        )
        output += devider
        filename = 'shoplist.txt'
        response = HttpResponse(output, content_type="text/plain")
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    @action(
        detail=True, methods=('POST', 'DELETE'),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        '''Add/Delete a recipe to/from favourites.'''
        data = {
            'user': request.user.id,
            'recipe': pk,
        }
        serializer = CheckFavouriteSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            return self.add_object(Favourites, request.user, pk)
        return self.delete_object(Favourites, request.user, pk)


class FollowViewSet(UserViewSet):
    '''Subscriptions viewset includes all actions.'''
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    @action(methods=('GET',), detail=False)
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(page,
                                      context={'request': request},
                                      many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        methods=('POST', 'DELETE'),
        detail=True)
    def subscribe(self, request, id=None):
        '''Follow the author.'''
        user = request.user
        author = get_object_or_404(UserCustomized, pk=id)
        data = {
            'user': user.id,
            'author': author.id,
        }
        serializer = CheckFollowSerializer(
            data=data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        if request.method == "POST":
            result = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(result, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        user.follower.filter(author=author).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    '''Ingredients' viewset. Ingredients Model. '''

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [IngredientsFilter]
    search_fields = ['^name']
    permission_classes = (IsAdminOrReadOnly,)
