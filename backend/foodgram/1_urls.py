from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.authtoken import views


router = routers.DefaultRouter()

# router.register(r'recipe', CatViewSet)
# router.register(r'ingredients', IngredientsViewSet)
# router.register(r'product', ProductViewSet, basename='Product')
# router.register(r'image', ImageViewSet, basename='Image')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/', include('recipes.urls', namespace='recipes')),
    path('api/', include('users.urls', namespace='users')),
    path('api/', include('djoser.urls')),  # Работа с пользователями.
    path('api/auth/', include('djoser.urls.authtoken')),  # Работа с токенами.
    # path('api/auth/token/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/auth/token/logout/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/auth/token/login/', views.obtain_auth_token),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
