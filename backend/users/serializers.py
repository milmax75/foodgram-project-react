from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from .models import UserCustomized
from .validators import validate_username
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from djoser.serializers import UserSerializer


'''class CustomUserSerializer(UserSerializer):
    class Meta:
        model = UserCustomized
        fields = ('email', 'password', 'username', 'first_name', 'last_name')''' 


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = UserCustomized
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
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


class GetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'email',
        )
        model = UserCustomized


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6,
        max_length=50,
        write_only=True,
        required=True,
        # validators=[validate_password]
    )
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserCustomized
        fields = ('old_password', 'password')

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
