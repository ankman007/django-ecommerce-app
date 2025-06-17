from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import Http404
from django.db.models import Count


def cart(request):
    return render(request, 'a_shop/cart.html')


def product_detail(request):
    return render(request, 'a_shop/product_detail.html')


def home(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=Count('products'))
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'a_shop/home.html', context)

