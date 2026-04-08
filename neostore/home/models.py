from django.db import models
from django.contrib.auth.models import AbstractUser

class Wallet(models.Model):
    money = models.IntegerField(verbose_name='Money', default=0)

class User(AbstractUser):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, verbose_name='Wallet', null=True, blank=True)
    date_birth = models.DateField(verbose_name='Date of birth', null=True)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type = models.BooleanField(verbose_name='Transaction type', default=True) # false stay for withdraw, true for top up
    amount = models.IntegerField(verbose_name='Amount', default=0)

class Thing(models.Model):
    value = models.IntegerField(verbose_name='Value', default=0)
    amount = models.IntegerField(verbose_name='Amount', default=0)
    photo = models.CharField(verbose_name='Photolink', max_length=100)
    name = models.CharField(verbose_name='Name', max_length=100)

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField(verbose_name='Is Checked', default=False)
    name = models.CharField(verbose_name='Name', max_length=100)
    givenfor = models.CharField(verbose_name='Given for', max_length=100)

class Order(models.Model):
    things = models.ManyToManyField(Thing)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Date of creation')
    state = models.BooleanField(verbose_name='Is ready', default=False)