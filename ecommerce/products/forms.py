
from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta: 
        model = Product
        fields = ['name', 'price', 'description', 'category', 'images', 'is_available', 'stock']
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']