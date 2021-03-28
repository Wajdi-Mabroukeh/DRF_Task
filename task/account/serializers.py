from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Account, Address
from django.contrib.auth.models import User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }


class AccountSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = Account
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data['user']
        account_type = validated_data['account_type']
        addresses = validated_data['addresses']

        user_data.pop('password2')
        password = user_data.pop('password')

        user = User.objects.create_user(**user_data)
        user.set_password(password)
        user.account.account_type = account_type

        if addresses:
            for address_temp in addresses:
                address, _ = Address.objects.get_or_create(city=address_temp.get('city'),
                                                           name=address_temp.get('name'),
                                                           country=address_temp.get('country'))
                user.account.addresses.add(address)

        user.save()

        return user.account
