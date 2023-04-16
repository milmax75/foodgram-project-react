from django.urls import path, include
from users.views import MyObtainTokenPairView, ChangePasswordView, RegisterViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

app_name = 'users'

router = DefaultRouter()

router.register('users', RegisterViewSet, basename='users')

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', RegisterView.as_view(), name='auth_register'),
    path(
        'change_password/<int:pk>/',
        ChangePasswordView.as_view(),
        name='auth_change_password'
    ),
    path('', include(router.urls)),
]
