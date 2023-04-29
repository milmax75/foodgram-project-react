
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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''Tags' viewset. Tags Model.'''

    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrReadOnly,)


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
        '''Retrieving objects for shoplist and favs'''
        if self.request.user.is_authenticated:
            return Recipe.objects.annotate(
                is_favorited=Exists(
                    Favourites.objects.filter(
                        user=self.request.user, recipe__pk=OuterRef('pk')
                    )
                ),
                is_in_shopcart=Exists(
                    ShopList.objects.filter(
                        user=self.request.user, recipe__pk=OuterRef('pk')
                    )
                ),
            )
        return Recipe.objects.annotate(
            is_favorited=Value(False, output_field=BooleanField()),
            is_in_shopcart=Value(False, output_field=BooleanField()),
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
            .values('ingredient__name', 'ingredient__units')
            .order_by('ingredient__name')
            .annotate(total=Sum('quantity'))
        )
        ingr_len = max(len(ingredient["ingredient__name"])
                       for ingredient in ingredients)
        total_len = max(len(str(ingredient["total"]))
                        for ingredient in ingredients)
        unit_len = max(len(ingredient["ingredient__units"])
                       for ingredient in ingredients)
        devider = (
            f'\n|{"_"*(ingr_len+2)}|{"_"*(total_len+2)}|{"_"*(unit_len+2)}|\n')
        output = 'The list of goods for your recipes. \n\n'
        output += f',{(len(devider)-devider.count("|"))*"_"},\n'
        output += devider.join(
                f'| {ingredient["ingredient__name"]} '
                f'{(ingr_len-len(ingredient["ingredient__name"]))*" "}'
                f'| {ingredient["total"]}'
                f'{(total_len-len(str(ingredient["total"])))*" "} '
                f'| {ingredient["ingredient__units"]}'
                f'{(unit_len-len(str(ingredient["ingredient__units"])))*" "} |'
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

    @action(
        methods=('POST', 'DELETE'),
        detail=True, permission_classes=(IsAuthenticated,)
    )
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

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        '''Subscribtions.'''
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    '''Ingredients' viewset. Ingredients Model. '''

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [IngredientsFilter]
    search_fields = ['^name']
    permission_classes = (IsAdminOrReadOnly,)
