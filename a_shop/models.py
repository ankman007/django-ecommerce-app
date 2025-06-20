from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from decimal import Decimal
from .utils import generate_short_uuid

class Category(models.Model):
    name = models.CharField(unique=True, max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Category: {self.name}"


class Product(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=22,
        unique=True,
        default=generate_short_uuid,
        editable=False
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        category_name = self.category.name if self.category else "Uncategorized"
        return f"Product: {self.name} (Category: {category_name})"
    
    class Meta:
        ordering = ['-id']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.alt_text:
            self.alt_text = slugify(self.product.name)
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart for {self.user.username} - Created at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_product')
    quantity = models.PositiveIntegerField()

    def subtotal(self):
        return self.quantity * Decimal(self.product.price)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Subtotal: ${self.subtotal():.2f})"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='pending', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment by {self.user.username} | ${self.total_price} | Status: {self.get_status_display()}"
