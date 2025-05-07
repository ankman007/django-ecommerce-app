from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from uuid import UUID
from loguru import logger


def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    print("Fetched products:", products)  
    context = {
        "page_title": "Products Page",
        "products": products,
        "categories": categories
    }
    print(f"context {context}")
    return render(request, 'index.html', context)
 
 
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        "page_title": "Products Page",
        "product": product,
    }
    return render(request, 'product_detail.html', context)


def product_category(request, category_name):
    products = Product.objects.filter(category__name=category_name)
    context = {
        "page_title": "Products Page",
        "products": products,
    }
    return render(request, 'product_category.html', context)