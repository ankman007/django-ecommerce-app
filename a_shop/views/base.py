from a_shop.models import Product, Category, Cart
from django.shortcuts import render
from django.db.models import Count

def home(request):
    products = Product.objects.all()
    categories = Category.objects.annotate(product_count=Count('products'))
    
    cart_product_ids = set()
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_product_ids = set(cart.items.values_list('product_id', flat=True))
        except Cart.DoesNotExist:
            cart_product_ids = set()
    else:
        session_cart = request.session.get('cart', {})
        cart_product_ids = set(pid for pid in session_cart.keys())
        
    context = {
        'products': products,
        'categories': categories,
        'cart_product_ids': cart_product_ids,  
    }
    return render(request, 'a_shop/home.html', context)


def contact(request):
    return render(request, 'a_shop/contact.html')


def about(request):
    return render(request, 'a_shop/about-us.html')


def privacy_policy(request):
    return render(request, 'a_shop/privacy-policy.html')
