from django.db import models
from django.contrib.auth.models import User  

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)  # Category name जैसे Vegetables, Fruits
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # new field

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # हर product किसी category में
    name = models.CharField(max_length=100)       # Product name
    description = models.TextField(blank=True)    # Optional description
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Product price
    stock = models.PositiveIntegerField(default=0)               # Stock quantity
    image = models.ImageField(upload_to='products/', blank=True) # Product image

    def __str__(self):
        return self.name  

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name