from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Address
from .serializers import AccountSerializer, UserSerializer


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

        user.account.account_type = account_type
        if addresses:
            for address_temp in addresses:
                address, _ = Address.objects.get_or_create(city=address_temp.get('city'),
                                                        name=address_temp.get('name'),
                                                        country=address_temp.get('country'))
                user.account.addresses.add(address)

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


class AccountList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        first_name = request.query_params.get('first_name')
        last_name = request.query_params.get('last_name')
        query = User.objects

        if username and username.strip():
            query = query.filter(username__contains=username)
        if first_name and first_name.strip():
            query = query.filter(first_name__contains=first_name)
        if last_name and last_name.strip():
            query = query.filter(last_name__contains=last_name)

        users = query.all()
        page = self.paginate_queryset(users)
        serializer = UserSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
