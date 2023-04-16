from rest_framework import generics

from rest_framework.permissions import IsAuthenticated, AllowAny

from recipes.models import UserCustomized

from .serializers import MyTokenObtainPairSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class ChangePasswordView(generics.UpdateAPIView):

    queryset = UserCustomized.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class MyObtainTokenPairView(TokenObtainPairView):

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
