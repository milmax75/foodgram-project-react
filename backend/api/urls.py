from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()


urlpatterns = [
    # Все зарегистрированные в router пути доступны в router.urls
    # Включены в головной urls.py
    #path('', include(router.urls)),
    # Работа с пользователями:
    path('', include('djoser.urls')),
    # Работа с токенами:
    path('auth/', include('djoser.urls.authtoken')),
]
