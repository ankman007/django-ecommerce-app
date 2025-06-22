from a_shop.models import Product, Category, Cart
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render

def category(request, slug):
    selected_category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=selected_category)
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
        'selected_category': selected_category.name,
        'cart_product_ids': cart_product_ids,  

    }
    return render(request, 'a_shop/home.html', context)