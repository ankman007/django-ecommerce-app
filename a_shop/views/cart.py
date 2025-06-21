from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from a_shop.models import Product, Cart, CartItem
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpResponse


def cart(request):
    cart_items = []

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.select_related('product').all()
        except Cart.DoesNotExist:
            cart_items = []
    else:
        session_cart = request.session.get('cart', {})
        product_ids = session_cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantity_map = {pid: qty for pid, qty in session_cart.items()}
        cart_items = [
            {'product': product, 'quantity': quantity_map[product.id]}
            for product in products
        ]

    return render(request, 'a_shop/cart.html', {'cart_items': cart_items})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            item.quantity += quantity
            item.save()
            total_items = sum(i.quantity for i in cart.items.all())
        else:
            cart_data = request.session.get('cart', {})
            cart_data[str(product_id)] = cart_data.get(str(product_id), 0) + quantity
            request.session['cart'] = cart_data
            total_items = sum(cart_data.values())
            
        button_html = render_to_string("a_shop/partials/add_to_cart_button.html", {
            "product": product,
            "added": True,
        })
        cart_count_html = render_to_string("a_shop/partials/cart_count.html", {
            "cart_count": total_items
        })

        return HttpResponse(button_html + cart_count_html)
