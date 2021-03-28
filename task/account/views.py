from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from .serializers import (
    AccountSerializer,
    UserSerializer, UserBasicInfoSerializer
)


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            user_serialized = UserSerializer(user)

            return Response({
                'user': user_serialized.data,
                'token': token.key
            }, status=HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)


class AccountListView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = UserBasicInfoSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'email']


class AccountInfoView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        account = self.serializer_class(request.user.account).data
        return Response(account, status=HTTP_200_OK)


class AccountAddressView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer

    def get(self, request, *args, **kwargs):
        account = self.serializer_class(request.user.account).data
        addresses = account.get('addresses')
        return Response(addresses, status=HTTP_200_OK)

