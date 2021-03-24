from rest_framework import serializers
from .models import Account, Address
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['county', 'name', 'city']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    addresses = AddressSerializer(many=True)

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'account_type', 'addresses')
        extra_kwargs = {
            'username': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        addresses = validated_data.pop('addresses')
        account_type = validated_data.pop('account_type')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        user.account.type = account_type;
        for address in addresses:
            Address.objects.create(account=user.account, **address)

        user.save()
        return user
