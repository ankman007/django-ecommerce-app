from django.urls import path
from .views import index, list_products, create_product, create_category, list_category

urlpatterns = [
    path('', index, name="index"),
    path('list/', list_products, name="product_list"),
    path('create/', create_product, name="create_product"),
    path('category/create/', create_category, name="create_category"),
    path('category/list/', list_category, name="category_list"),
]