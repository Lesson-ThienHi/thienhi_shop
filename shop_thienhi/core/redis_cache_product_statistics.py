from shop_thienhi.redis import redis_client
from shop_thienhi.utils import constant
import json


def create_key_product_statistics(key: str):
    return f"{key}"


def format_cache_data_product_statistics(data):
    list_data = []
    for item in data:
        value = {
            'product': item['product'],
            'number_of_sold': item['number_of_sold'],
            "total_money": item["total_money"],
            "timestamp": item["timestamp"]
        }
        list_data.append(value)
    return json.dumps(list_data)


def create_cached_device_product_statistics(data):
    print("CREATE REDIS_CACHE_PRODUCT_STATISTICS")
    key = create_key_product_statistics(constant.REDIS_CACHE_PRODUCT_STATISTICS)
    v = format_cache_data_product_statistics(data)
    return redis_client.getset(key,v)


def get_cached_device_product_statistics():
    key = f'{constant.REDIS_CACHE_PRODUCT_STATISTICS}'
    cached = redis_client.get(key)
    tmp = {}
    if not cached:
        return tmp
    else:
        tmp[key] = json.loads(cached.decode('utf-8'))
        return tmp


def remove_cached_device_product_statistics():
    print("REMOVE REDIS_CACHE_PRODUCT_STATISTICS")
    key = create_key_product_statistics(constant.REDIS_CACHE_PRODUCT_STATISTICS)
    return redis_client.delete(key)