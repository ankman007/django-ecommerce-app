from django.shortcuts import render, get_object_or_404
from a_shop.models import Product, Category, Cart
from django.db.models import Q
from loguru import logger

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    
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
        
    return render(request, 'a_shop/product_detail.html', {
        'product': product,
        'similar_products': similar_products,
        'cart_product_ids': cart_product_ids,  
    })


def product_search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else []
    categories = Category.objects.all()
    
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
        
    return render(request, 'a_shop/home.html', {
        'query': query,
        'products': results,
        'categories': categories,
        'cart_product_ids': cart_product_ids,  
    })
