from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status, generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from .models import UserCustomized, Follow

from .serializers import (
    MyTokenObtainPairSerializer,
    ChangePasswordSerializer,
    PostUserSerializer,
    GetUserSerializer,
    MeSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView


class ChangePasswordView(generics.UpdateAPIView):

    queryset = UserCustomized.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class MyObtainTokenPairView(TokenObtainPairView):

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PostUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserCustomized.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return PostUserSerializer
        return GetUserSerializer

    @action(detail=False, methods=('get', ),
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        myself = UserCustomized.objects.get(username=request.user.username)
        return Response(MeSerializer(myself).data, status=status.HTTP_200_OK)
