from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from users.models import UserCustomized, Follow
from users.validators import validate_username
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import UserSerializer, UserCreateSerializer


class PostUserSerializer(UserCreateSerializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = UserCustomized
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def create(self, validated_data):
        user = UserCustomized.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class GetUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = UserCustomized
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj.id).exists()
