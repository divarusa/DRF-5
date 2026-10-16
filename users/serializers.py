from rest_framework import serializers  # type: ignore[reportMissingImports]
from django.contrib.auth.models import User
from .models import ConfirmationCode


class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField()

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже существует.")
        return username


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ConfirmValidateSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate_code(self, code):
        if not ConfirmationCode.objects.filter(code=code).exists():
            raise serializers.ValidationError("Неверный код подтверждения.")
        return code