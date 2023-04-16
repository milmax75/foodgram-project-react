from rest_framework import generics, viewsets

from djoser.views import UserViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from recipes.models import UserCustomized

from .serializers import (
    MyTokenObtainPairSerializer,
    ChangePasswordSerializer,
    #CustomUserSerializer,
    UserSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


class ChangePasswordView(generics.UpdateAPIView):

    queryset = UserCustomized.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class MyObtainTokenPairView(TokenObtainPairView):

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


'''class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)'''


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
