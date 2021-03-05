from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
