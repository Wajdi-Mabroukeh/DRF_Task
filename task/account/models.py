from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

account_type = (
    ('ADMIN', 'admin'),
    ('CLIENT', 'client')
)


class Address(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta:
        unique_together = [['name', 'city', 'country']]
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.name}, {self.city}, {self.county}'


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=50, null=True, choices=account_type)
    addresses = models.ManyToManyField(Address, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
    instance.account.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
