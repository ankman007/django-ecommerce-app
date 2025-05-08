from .models import Product
from django.db import models

class Cart(models.Model):
    user = models.ForeignKey()
    created_at = models.DateTimeField(auto_now_add=True)