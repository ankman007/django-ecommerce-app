from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import Http404
from django.db.models import Count
from loguru import logger


def home(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=Count('products'))
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'a_shop/home.html', context)


def category(request, slug):
    selected_category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=selected_category)
    categories = Category.objects.annotate(product_count=Count('products'))

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category.name,
    }
    return render(request, 'a_shop/home.html', context)
    
    
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    context = {
        'product': product,
        'similar_products': similar_products
    }
    return render(request, 'a_shop/product_detail.html', context)


def cart(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'a_shop/cart.html', context)