import json

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Account, Address
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token

from .serializers import AccountSerializer


def is_validate(**kwargs):
    if kwargs['password'] != kwargs['password2']:
        raise ValidationError({"password": "Password fields didn't match."})

    try:
        validate_email(kwargs['email'])
    except ValidationError:
        raise ValidationError({"email": "email format not correct"})

    if User.objects.filter(username=kwargs['username']).exists():
        raise ValidationError({"username": "username exists before. try another one"})

    if User.objects.filter(email=kwargs['email']).exists():
        raise ValidationError({"email": "email exists before. try another one"})

    return True


class RegisterView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        email = request.data.get('email')
        addresses = request.data.get('addresses')
        account_type = request.data.get('account_type')

        # validation
        is_validate(password=password, password2=password2,
                    email=email, username=username)

        # create new user
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()

        user.account.account_type = account_type
        if addresses:
            for address_temp in addresses:
                Address.objects.get_or_create(account=user.account,
                                              city=address_temp.get('city'),
                                              name=address_temp.get('name'),
                                              county=address_temp.get('country'))

        user.save()
        data = AccountSerializer(user.account).data

        return Response(data=data, status=status.HTTP_201_CREATED)


class LoginView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            data = {"username": user.username, "token": str(token)}
            return JsonResponse(data)
        else:
            raise ValidationError({"login": "invalid login"})
