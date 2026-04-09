from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class Wallet(models.Model):
    money = models.IntegerField(verbose_name='Money', default=0)


class User(AbstractUser):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, verbose_name='Wallet', null=True, blank=True)
    date_birth = models.DateField(verbose_name='Date of birth', null=True)


class Thing(models.Model):
    value = models.IntegerField(verbose_name='Value', default=0)
    amount = models.IntegerField(verbose_name='Amount', default=0)
    photo = models.ImageField(verbose_name='Photolink', upload_to='things/', null=True, blank=True)
    name = models.CharField(verbose_name='Name', max_length=100)

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        return '/static/images/no-image.jpg'


class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.BooleanField(verbose_name='Is Checked', default=False)
    name = models.CharField(verbose_name='Name', max_length=100)
    givenfor = models.CharField(verbose_name='Given for', max_length=100)
    date = models.DateTimeField(verbose_name='Date of birth', null=True, auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Date of creation', auto_now_add=True)
    state = models.BooleanField(verbose_name='Is ready', default=False)

    @property
    def total(self):
        total_sum = 0
        for item in self.items.all():
            price = item.price if item.price else item.thing.value
            total_sum += item.quantity * price
        return total_sum


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    @property
    def subtotal(self):
        return self.quantity * self.price


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    thing = models.ForeignKey('Thing', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.thing.value * self.quantity


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
