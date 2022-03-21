from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    product_type = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True, default=0)
    unit = models.CharField(max_length=255, null=True, blank=True, default="$")
    accessory = models.CharField(max_length=255, null=True, blank=True)                 # Phụ kiện

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    total = models.FloatField(null=True, blank=True, default=0)
    money_received = models.FloatField(null=True, blank=True)
    refunds = models.FloatField(null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    product = models.ForeignKey(Product, related_name='product_order_detail',blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True, blank=True)
    into_money = models.FloatField(null=True, blank=True)
    order = models.ForeignKey(Order, related_name='order',blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.FloatField(null=True)

    def __str__(self):
        return str(self.id)


class ProductStatistics(models.Model):
    product = models.ForeignKey(Product, related_name='product_statistics',blank=True, null=True, on_delete=models.SET_NULL)
    number_of_sold = models.IntegerField(null=True, blank=True, default=0)
    total_money = models.FloatField(null=True, blank=True, default=0)
    timestamp = models.FloatField(null=True)


class CustomerStatistics(models.Model):
    age = models.IntegerField(null=True, blank=True, default=0)
    number_of_sold = models.IntegerField(null=True, blank=True, default=0)
    total_money = models.FloatField(null=True, blank=True, default=0)
    timestamp = models.FloatField(null=True)
