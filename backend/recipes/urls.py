from django.urls import path, include
from .views import (
    IngredientsViewSet,
    TagViewSet,
    FavouritesViewSet,
    ShopListViewSet
)
from rest_framework.routers import DefaultRouter


app_name = 'recipes'

router = DefaultRouter()

router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('tag', TagViewSet, basename='tag')
router.register('favourites', FavouritesViewSet, basename='favourites')
router.register('shoplist', ShopListViewSet, basename='shoplist')


urlpatterns = (
    path('', include(router.urls)),
)
