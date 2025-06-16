from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = 'shop'

urlpatterns = [
    path('/', product_list, name="list_products"),
    path('/<product_id>/detail/', product_detail, name="product_detail"),
]

