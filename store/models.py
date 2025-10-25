from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)  # varchar(255)
    description = models.TextField()  # text
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # decimal(10,2)
    inventory = models.IntegerField()  # integer
    last_update = models.DateTimeField(auto_now=True)  # timestamp


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, )
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=MEMBERSHIP_BRONZE,
    )
