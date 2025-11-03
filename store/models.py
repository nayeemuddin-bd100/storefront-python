from django.db import models

# Create your models here.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # ForeignKey - Many Collections can point to ONE Product
    # related_name='+' means no reverse relation (can't access collection from product)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:  # Returns string representation for admin/debugging (shows "Electronics" instead of "Collection object (1)")
        return self.title

    # Returns developer-friendly representation for debugging in shell/logs
    def __repr__(self) -> str:
        return f"<Collection(id={self.pk}, title='{self.title}')>"

    class Meta:
        ordering = ['title']  # Sort by title A-Z
        verbose_name = 'Collection'  # Singular name shown in Django admin
        verbose_name_plural = 'Collections'  # Plural name shown in Django admin


class Product(models.Model):
    title = models.CharField(max_length=255)  # varchar(255)
    description = models.TextField()  # text
    price = models.DecimalField(
        max_digits=10, decimal_places=2)  # decimal(10,2)
    inventory = models.IntegerField()  # integer
    last_update = models.DateTimeField(auto_now=True)  # timestamp
    # ForeignKey - Many Products belong to ONE Collection
    # related_name='products' allows: collection.products.all() to get all products
    # on_delete=PROTECT prevents deleting a collection if it has products
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products', null=True)

    def __str__(self) -> str:  # Returns string representation showing product title in admin/debugging
        return self.title

    # Returns detailed representation for developers including id and price
    def __repr__(self) -> str:
        return f"<Product(id={self.pk}, title='{self.title}', price={self.price})>"

    @property
    # Property that returns True if inventory is less than 10 (access like: product.is_low_stock)
    def is_low_stock(self) -> bool:
        return self.inventory < 10

    @property
    # Property that returns True if product has inventory (access like: product.is_in_stock)
    def is_in_stock(self) -> bool:
        return self.inventory > 0

#      @property converts a method into a read-only attribute. You can access
#   it without parentheses, like a regular field.

#   Usage:
#   product = Product.objects.get(id=1)

#   # Without @property (as a regular method):
#   product.is_low_stock()  # ❌ Need parentheses

#   # With @property:
#   product.is_low_stock  # ✅ Access like an attribute!
#   product.is_in_stock   # ✅ No parentheses needed

    class Meta:
        ordering = ['title']  # Default sort order: alphabetical by title
        verbose_name = 'Product'  # Singular name in admin
        verbose_name_plural = 'Products'  # Plural name in admin
        # Database index for faster title searches
        indexes = [models.Index(fields=['title'])]


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

    # Returns full name for admin/debugging (shows "John Doe" instead of "Customer object (1)")
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # Returns detailed representation including id, name, and membership level
    def __repr__(self) -> str:
        return f"<Customer(id={self.pk}, name='{self.first_name} {self.last_name}', membership='{self.membership}')>"

    @property
    def full_name(self) -> str:  # Property that returns full name (access like: customer.full_name)
        return f"{self.first_name} {self.last_name}"

    class Meta:
        # Default sort order: by last name, then first name (like a phonebook)
        ordering = ['last_name', 'first_name']
        verbose_name = 'Customer'  # Singular name in admin
        verbose_name_plural = 'Customers'  # Plural name in admin
        # Database index for faster email lookups
        indexes = [models.Index(fields=['email'])]


class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    # ForeignKey - Many Orders belong to ONE Customer
    # related_name='orders' allows: customer.orders.all() to get all customer orders
    # This is a REVERSE relationship (use prefetch_related for optimization)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='orders')


class Review(models.Model):
    # ForeignKey - Many Reviews belong to ONE Product
    # related_name='reviews' allows: product.reviews.all() to get all reviews for a product
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
