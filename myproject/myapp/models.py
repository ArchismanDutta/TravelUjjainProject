from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils import timezone
from decimal import Decimal


class Customer(AbstractUser):
    customer_number = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.customer_number:
            self.customer_number = get_random_string(length=8).upper()
        super().save(*args, **kwargs)


class TravelPackage(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.CharField(max_length=50)  # e.g., "2 Days / 1 Night"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='packages/')

    def __str__(self):
        return self.title


class Car(models.Model):
    vehicle_type = models.CharField(max_length=100)  # e.g., "SUV", "Sedan"
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return self.vehicle_type


class Addon(models.Model):
    PHOTOGRAPHY_TYPES = [
        ('candid', 'Candid'),
        ('traditional', 'Traditional'),
        ('drone', 'Drone'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='addons/')
    photograph_type = models.CharField(max_length=20, choices=PHOTOGRAPHY_TYPES)
    reel_edit = models.BooleanField(default=False)
    reel_edit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional: Only if reel edit is selected"
    )

    def __str__(self):
        return self.title

    def total_price(self):
        base = self.price or Decimal('0.00')
        extra = self.reel_edit_price if self.reel_edit and self.reel_edit_price else Decimal('0.00')
        return base + extra


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    travel_package = models.ForeignKey(TravelPackage, on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True, blank=True)
    addons = models.ManyToManyField(Addon, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def calculate_total(self):
        total = Decimal('0.00')
        if self.travel_package and self.travel_package.price:
            total += self.travel_package.price
        if self.car and self.car.price:
            total += self.car.price
        for addon in self.addons.all():
            total += addon.total_price()
        return total

    def __str__(self):
        return f"Cart of {self.user.username} (#{self.pk})"
