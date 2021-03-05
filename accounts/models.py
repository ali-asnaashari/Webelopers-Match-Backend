from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()


class Rate(models.Model):
    rate_number = models.PositiveBigIntegerField(default=0)


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    tag = models.ManyToManyField(Tag)
    comments = models.ManyToManyField(Comment)
    product_image = models.ImageField(upload_to='images/', blank=True)
    rate = models.ManyToManyField(Rate)


    def __str__(self):
        return self.name


class ShoppingCard(models.Model):
    user = models.ManyToManyField(User)
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    buy_quantity=models.IntegerField()


