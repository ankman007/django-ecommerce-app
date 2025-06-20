from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('product/<str:id>', product_detail, name='product_detail'),
    path('category/<slug:slug>', category, name='category'),
    path('cart/', cart, name='cart'),
    path('add-to-cart/<str:product_id>/', add_to_cart, name='add_to_cart'),
]

