from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('product/<str:id>', product_detail, name='product_detail'),
    path('category/<slug:slug>', category, name='category'),
]

