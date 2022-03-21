from django.contrib import admin
from .models import Product, Order, OrderDetails, ProductStatistics, CustomerStatistics 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "price", "size", "product_type", "unit", "accessory"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "total", "money_received", "refunds", "created_at", "created_by"]


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "quantity", "into_money", "order"]

@admin.register(ProductStatistics)
class ProductStatisticsAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "number_of_sold", "total_money", "timestamp"]

@admin.register(CustomerStatistics)
class CustomerStatisticsAdmin(admin.ModelAdmin):
    list_display = ["id", "age", "number_of_sold", "total_money", "timestamp"]