from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.first_name


class Product(models.Model):
    CATEGORY_CHOICE = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
        ('Anywhere', 'Anywhere'),
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Orders(models.Model):
    STATUS_CHOICES = (
        ('Delivered', 'Delivered'),
        ('Pending', 'Pending'),
        ('Outfordelivery', 'Outfordelivery')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=100)
    created_date = models.DateField(auto_now_add=True, null=True)
