from django.contrib import admin
from .models import Product , Category,Customer, Cart , CartItem

class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category_name')  # Ensure 'category_name' is correct

    def category_name(self, obj):
        return obj.category.name  # Ensure this method is present in AdminProduct

    category_name.short_description = 'Category Name'  # Optional: customize the column header

admin.site.register(Product, AdminProduct)
admin.site.register(Customer)
admin.site.register(Category)
# store/admin.py

admin.site.register(Cart)
admin.site.register(CartItem)
