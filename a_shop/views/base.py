from a_shop.models import Product, Category, Cart
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Count
from a_shop.forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import os
from dotenv import load_dotenv
from pathlib import Path

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
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            BASE_DIR = Path(__file__).resolve().parent.parent
            load_dotenv(os.path.join(BASE_DIR, '.env'))
            RECIPIENT_EMAIL  = os.getenv('RECIPIENT_EMAIL')
            
            subject = f"New contact us message from {form.cleaned_data['name']}"
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['email']
            full_message = f"From: {form.cleaned_data['name']} <{sender_email}>\n\n{message}"
            
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [RECIPIENT_EMAIL],
                fail_silently=False,
            )
            toast_message = "Your message has been sent successfully! <a href='/contact/' class='underline'>Send another?</a>"
            toast_html = render_to_string("a_shop/partials/toast.html", {"message": toast_message})
            messages.success(request, toast_html)
            return redirect('home')
    else:
        form = ContactForm()

    return render(request, 'a_shop/contact.html', {'form': form})


def contact_success(request):
    return HttpResponse("Thanks for contacting us!")


def about(request):
    return render(request, 'a_shop/about-us.html')


def privacy_policy(request):
    return render(request, 'a_shop/privacy-policy.html')
