from django.shortcuts import render, get_object_or_404
from a_shop.models import Product, Category
from django.db.models import Q

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)
    return render(request, 'a_shop/product_detail.html', {
        'product': product,
        'similar_products': similar_products
    })


def product_search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else []
    categories = Category.objects.all()
    return render(request, 'a_shop/home.html', {
        'query': query,
        'products': results,
        'categories': categories
    })
