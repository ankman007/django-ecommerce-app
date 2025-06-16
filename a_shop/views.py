from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import Http404


def cart(request):
    return render(request, 'a_shop/cart.html')


def product_detail(request):
    return render(request, 'a_shop/product_detail.html')


def product_list(request):
    item_count = range(1, 20)
    context = {'quantity': item_count}
    return render(request, 'a_shop/product_list.html', context)

