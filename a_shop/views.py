from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import Http404
from django.db.models import Count
from loguru import logger
from django.template.loader import render_to_string
from django.http import HttpResponse

def home(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=Count('products'))
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'a_shop/home.html', context)


def contact(request):
    return render(request, 'a_shop/contact.html')


def about(request):
    return render(request, 'a_shop/about-us.html')


def privacy_policy(request):
    return render(request, 'a_shop/privacy-policy.html')


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


from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Cart, CartItem

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        cart_item.quantity += quantity
        cart_item.save()

    cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({
        "cart_count_html": render_to_string("a_shop/partials/cart_count.html", {"cart_count": cart_count}),
        "button_html": render_to_string("a_shop/partials/add_to_cart_button.html", {"product_id": product_id})
    })
