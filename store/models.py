from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Product
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    # image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# class Product(models.Model):
    # ... your existing fields ...
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            # Return an empty string or a path to a default image
            url = 'https://via.placeholder.com/300' 
        return url

# Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

# CartItem
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

# Order
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)

# OrderItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


# In store/models.py

class CartItem(models.Model):
    # Change from product = models.ForeignKey(Product, ...)
    # To this (using a string):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    # ... rest of fields