from django.urls import path
from .views import index, product_detail

urlpatterns = [
    path('', index, name="index"),
]