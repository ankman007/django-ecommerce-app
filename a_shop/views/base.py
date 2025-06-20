from a_shop.models import Product, Category
from django.shortcuts import render
from django.db.models import Count

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
