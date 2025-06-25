from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest
import stripe
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    if request.method == "POST":
        item_names = request.POST.getlist("items_name")
        item_prices = request.POST.getlist("items_price")
        item_quantities = request.POST.getlist("items_quantity")

        if not item_names or not item_prices or not item_quantities:
            return HttpResponseBadRequest("Missing form data")

        line_items = []
        for name, price, quantity in zip(item_names, item_prices, item_quantities):
            try:
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(float(price) * 100),
                        'product_data': {
                            'name': name,
                        },
                    },
                    'quantity': int(quantity),
                })
            except ValueError:
                return HttpResponseBadRequest("Invalid price or quantity")

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )
        return redirect(checkout_session.url)

    return HttpResponseBadRequest("Invalid request method")


def success(request):
    toast_message = "Payment successful!"
    toast_html = render_to_string("a_shop/partials/toast.html", {"message": toast_message})
    messages.success(request, toast_html)
    return redirect('home')


def cancel(request):
    toast_message = "❌ Payment was canceled. <a href='/cart/' class='underline'>Return to cart</a> to try again."
    toast_html = render_to_string("a_shop/partials/toast.html", {"message": toast_message})
    messages.error(request, toast_html)
    return redirect('home')
