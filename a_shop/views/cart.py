from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from a_shop.models import Product, Cart, CartItem
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.http import HttpResponse


def cart(request):
    products = Product.objects.all()
    return render(request, 'a_shop/cart.html', {'products': products})


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
