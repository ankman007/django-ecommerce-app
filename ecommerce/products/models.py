import uuid
import hashlib
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django import forms

class Category(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=250, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    
class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=250, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    images = models.ImageField(upload_to="images/", null=True, blank=True)
    seo_slug = models.SlugField()
    is_available = models.BooleanField(default=True)
    stock = models.PositiveBigIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.seo_slug:
            truncated_title = self.title[:40]  
            self.seo_slug = f"{slugify(truncated_title)}--{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        super(Product, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ['created_at']
        
    

