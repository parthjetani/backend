from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    age = models.CharField(max_length=3, blank=False)

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    street = models.CharField(max_length=500, blank=False)
    city = models.CharField(max_length=100, blank=False)
    country = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=12, blank=False)


class Vehicle(models.Model):
    user = models.ForeignKey(User, related_name="car", on_delete=models.CASCADE)
    number_plate = models.CharField(max_length=30, blank=False)
    model = models.CharField(max_length=50, blank=False)
    brand = models.CharField(max_length=50, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model


def nameFile(instance, filename):
    return "/".join(["images", str(instance.title), filename])


class Ads(models.Model):
    author = models.ManyToManyField(User, related_name="ads")
    title = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    vehicle = models.ManyToManyField(Vehicle, related_name="ads_vehicle")
    file = models.ImageField(upload_to=nameFile, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
