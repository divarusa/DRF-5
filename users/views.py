import random

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ConfirmationCode
from .serializers import (
    UserValidateSerializer, UserLoginSerializer, ConfirmValidateSerializer
)


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.create_user(username=username, password=password, is_active=False)

        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        ConfirmationCode.objects.create(user=user, code=code)

        return Response(
            data={'user_id': user.id, 'confirmation_code': code},
            status=status.HTTP_201_CREATED
        )


class AuthorizationAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        user = authenticate(
            username=serializer.validated_data.get('username'),
            password=serializer.validated_data.get('password')
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        return Response(
            data={'error': 'Неверные данные или пользователь не подтверждён'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class ConfirmAPIView(APIView):
    def post(self, request):
        serializer = ConfirmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        code = serializer.validated_data.get('code')
        confirmation = ConfirmationCode.objects.get(code=code)

        user = confirmation.user
        user.is_active = True
        user.save()
        confirmation.delete()

        return Response(data={'message': 'Пользователь подтверждён'})
