from django.contrib import admin
from .models import Customer, Product, Category, Cart, Cartitems

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Cartitems)