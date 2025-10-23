from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)  # varchar(255)
    description = models.TextField()  # text
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # decimal(10,2)
