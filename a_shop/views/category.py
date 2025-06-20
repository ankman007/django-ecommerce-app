from a_shop.models import Product, Category
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render

def category(request, slug):
    selected_category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=selected_category)
    categories = Category.objects.annotate(product_count=Count('products'))

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category.name,
    }
    return render(request, 'a_shop/home.html', context)