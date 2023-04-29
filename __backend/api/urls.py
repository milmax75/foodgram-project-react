from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, RecipeViewSet, IngredientsViewSet, FollowViewSet

app_name = 'api'

router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('users', FollowViewSet, basename='users')


urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включены в головной urls.py
    path('', include(router.urls)),
    # Работа с пользователями:
    path('', include('djoser.urls')),
    # Работа с токенами:
    path('auth/', include('djoser.urls.authtoken')),
]
