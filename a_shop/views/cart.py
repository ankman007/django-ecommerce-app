from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from a_shop.models import Product, Cart, CartItem
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from loguru import logger


def cart(request):
    logger.info("Cart view accessed")
    cart_items = []

    if request.user.is_authenticated:
        logger.info(f"User {request.user} is authenticated")
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.select_related('product').all()
            logger.debug(f"Cart items from DB: {[{'product': item.product.name, 'quantity': item.quantity} for item in cart_items]}")
        except Cart.DoesNotExist:
            logger.warning("Cart does not exist for user")
            cart_items = []
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
    else:
        logger.info("Anonymous user detected")
        session_cart = request.session.get('cart', {})
        logger.debug(f"Session cart data: {session_cart}")
        product_ids = session_cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantity_map = {pid: qty for pid, qty in session_cart.items()}
        cart_items = [
            {'product': product, 'quantity': quantity_map[product.id]}
            for product in products
        ]
        logger.debug(f"Session-based cart items: {cart_items}")
        subtotal = sum(item['product'].price * item['quantity'] for item in cart_items)

    shipping = 5.00
    total = float(subtotal) + float(shipping)

    return render(request, 'a_shop/cart.html', {
        'cart_items': cart_items,
        'shipping_cost': shipping,
        'subtotal': subtotal,
        'total': total,
    })


def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        logger.info(f"Adding product {product.name} (ID: {product_id}) with quantity {quantity}")

        if request.user.is_authenticated:
            logger.info(f"User {request.user} is authenticated")
            cart, created = Cart.objects.get_or_create(user=request.user)
            if created:
                logger.debug("New cart created for user")
            item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
            item.quantity += quantity
            item.save()
            total_items = sum(i.quantity for i in cart.items.all())
            logger.debug(f"Updated cart item: {product.name}, total quantity: {item.quantity}")
            logger.debug(f"Total items in authenticated user's cart: {total_items}")
        else:
            logger.info("Anonymous user - updating session cart")
            cart_data = request.session.get('cart', {})
            old_qty = cart_data.get(str(product_id), 0)
            cart_data[str(product_id)] = old_qty + quantity
            request.session['cart'] = cart_data
            total_items = sum(cart_data.values())
            logger.debug(f"Session cart updated: {cart_data}")
            logger.debug(f"Total items in session cart: {total_items}")

        button_html = render_to_string("a_shop/partials/add_to_cart_button.html", {
            "product": product,
            "added": True,
        })
        cart_count_html = render_to_string("a_shop/partials/cart_count.html", {
            "cart_count": total_items
        })

        return HttpResponse(button_html + cart_count_html)


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = cart.items.get(product=product)
            cart_item.delete()
        except Cart.DoesNotExist:
            pass
    else:
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        if product_id_str in cart:
            del cart[product_id_str]
            request.session['cart'] = cart

    return redirect('cart')