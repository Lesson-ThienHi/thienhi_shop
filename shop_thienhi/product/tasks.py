from config import celery_app
from celery import shared_task
from shop_thienhi.utils import constant
from shop_thienhi.utils.format_time import format_time_filter
from shop_thienhi.product.models import Product, ProductStatistics, CustomerStatistics, OrderDetails, Order
from django.db.models.aggregates import Sum
import datetime

@shared_task(name=constant.CELERY_TASK_PRODUCT_STATISTICS)
def product_statistics():
    time_date = format_time_filter()
    products = Product.objects.all()
    for product in products:
        order_details = OrderDetails.objects.filter(
            product=product.id, 
            timestamp__range=[time_date['start_time'], time_date['end_time']]
        ).aggregate(
            number_of_sold = Sum('quantity'),
            total_money = Sum('into_money')
        )
        ProductStatistics.objects.update_or_create(
            product = product,
            timestamp = time_date['start_time'],
            defaults = {
                'product' : product,
                'number_of_sold' : order_details['number_of_sold'],
                'total_money' : order_details['total_money'],
                'timestamp': time_date['start_time']
            }
        )
    return "CELERY TASK PRODUCT STATISTICS SUCCESS"


@shared_task(name=constant.CELERY_TASK_CUSTOMER_STATISTICS)
def customer_statistics():
    time_date = format_time_filter()
    products = Product.objects.all()
    for product in products:
        order_details = OrderDetails.objects.filter(
            product=product.id, 
            time_stamp__range=[time_date['start_time'], time_date['end_time']]
        ).aggregate(
            number_of_sold = Sum('quantity'),
            total_money = Sum('into_money')
        )
        ProductStatistics.objects.update_or_create(
            product = product,
            timestamp = time_date['start_time'],
            defaults = {
                'product' : product,
                'number_of_sold' : order_details['number_of_sold'],
                'total_money' : order_details['total_money'],
                'timestamp': time_date['start_time']
            }
        )
    return "CELERY TASK PRODUCT STATISTICS SUCCESS"