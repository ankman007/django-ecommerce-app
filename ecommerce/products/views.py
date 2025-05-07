from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm, CategoryForm
from uuid import UUID


def index(request):
    products = Product.objects.all()
    print("Fetched products:", products)  
    context = {
        "page_title": "Products Page",
        "products": products
    }
    print(f"context {context}")
    return render(request, 'index.html', context)
 
 
def product_detail(request, id):
    # Convert the id to UUID
    product_id = UUID(id)
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})