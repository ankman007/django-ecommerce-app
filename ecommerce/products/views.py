from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm, CategoryForm

def index(request):
    user = request.GET.get('name', 'Guest')
    context = {
        'page_title': 'Product Page',
        'user': user
    }
    return render(request, 'index.html', context)


def list_products(request):
    products = Product.objects.all()
    print("Fetched products:", products)  
    context = {
        "page_title": "Product List",
        "data": products
    }
    print(f"context {context}")
    return render(request, 'product_list.html', context)
    
    
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    context = {
        "page_title": "Create Product",
        "form": form
    }
    return render(request, 'create_product.html', context)

