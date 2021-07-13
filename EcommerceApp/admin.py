from django.contrib import admin
from .models import Customer, Product, Orders


class AdminCustomer(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'location', 'mobile']


class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'description', 'category']


class AdminOrders(admin.ModelAdmin):
    list_display = ['customer','product','status','created_date']


admin.site.register(Customer, AdminCustomer)
admin.site.register(Product, AdminProduct)
admin.site.register(Orders, AdminOrders)
