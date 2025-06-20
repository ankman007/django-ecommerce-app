from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from a_shop.models import Product, Cart, CartItem


def cart(request):
    products = Product.objects.all()
    return render(request, 'a_shop/cart.html', {'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))

    cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({
        "cart_count_html": render_to_string("a_shop/partials/cart_count.html", {"cart_count": cart_count}),
        "button_html": render_to_string("a_shop/partials/add_to_cart_button.html", {"product_id": product_id})
    })
