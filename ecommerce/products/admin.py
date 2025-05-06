from django.contrib import admin
from .models import Category, Product
from django.utils.html import mark_safe

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)  
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_available', 'stock', 'created_at', 'image_preview')  
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'is_available')
    ordering = ['-created_at']
    prepopulated_fields = {'seo_slug': ('title',)}
    list_editable = ('is_available', 'stock')

    def image_preview(self, obj):
        if obj.images:
            return mark_safe(f'<img src="{obj.images.url}" width="50" height="50" />')
        return "-"
    image_preview.short_description = 'Image Preview'

admin.site.register(Product, ProductAdmin)
