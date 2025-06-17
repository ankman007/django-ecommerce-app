from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('cart/', cart, name='cart'),
    path('detail/', product_detail, name='product_detail'),
]

