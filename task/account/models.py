from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Address(models.Model):
    name = models.CharField(max_length=200, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    county = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['name', 'city', 'county']]
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.name}, {self.city.name}, {self.county.name}'


class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.ForeignKey(AccountType, null= True, on_delete=models.SET_NULL)
    addresses = models.ManyToManyField(Address)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
    instance.account.save()

@receiver(post_save, sender=Account)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
