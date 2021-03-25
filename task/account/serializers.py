from rest_framework import serializers
from .models import Account, Address
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'



class AccountSerializer(serializers.ModelSerializer):


    class Meta:
        model = Account
        fields = '__all__'

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #
    #     return attrs
    #
    # def create(self, validated_data):
    #     addresses = validated_data.pop('addresses')
    #     account_type = validated_data.pop('account_type')
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )
    #
    #     user.set_password(validated_data['password'])
    #     user.save()
    #
    #     user.account.type = account_type;
    #     for address in addresses:
    #         Address.objects.create(account=user.account, **address)
    #
    #     user.save()
    #     return user
