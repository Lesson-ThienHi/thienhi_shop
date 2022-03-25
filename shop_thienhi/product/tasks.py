from config import celery_app
from celery import shared_task
from shop_thienhi.utils import constant
from shop_thienhi.utils.format_time import format_time_filter
from shop_thienhi.product.models import Product, ProductStatistics, CustomerStatistics, OrderDetails, Order
from django.db.models.aggregates import Sum
import datetime
from shop_thienhi.core.redis_cache_product_statistics import create_cached_device_product_statistics

@shared_task(name=constant.CELERY_TASK_PRODUCT_STATISTICS)
def product_statistics():
    list_data = []
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
        product_is_exit = ProductStatistics.objects.filter(product=product, timestamp = time_date['start_time']).first()
        if product_is_exit:
            product_is_exit.number_of_sold = order_details['number_of_sold'] if order_details else 0
            product_is_exit.total_money = order_details['total_money'] if order_details else 0
            product_is_exit.save()
            data = {
                'product' : product_is_exit.product.name,
                'number_of_sold' : product_is_exit.number_of_sold,
                'total_money' : product_is_exit.total_money,
                'timestamp': product_is_exit.timestamp
            }
            list_data.append(data)
        else:
            data_product_statistic = ProductStatistics.objects.create(
                product = product,
                number_of_sold = order_details['number_of_sold'] if order_details else 0,
                total_money = order_details['total_money'] if order_details else 0,
                timestamp = time_date['start_time']
            )
            data = {
                'product' : data_product_statistic.product.name,
                'number_of_sold' : data_product_statistic.number_of_sold,
                'total_money' : data_product_statistic.total_money,
                'timestamp': data_product_statistic.timestamp
            }
            list_data.append(data)
    create_cached_device_product_statistics(list_data)
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