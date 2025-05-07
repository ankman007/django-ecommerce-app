from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('category/<str:category_name>/', views.product_category, name="product_category"),
    path('<int:product_id>/', views.product_detail, name="product_detail"),
]