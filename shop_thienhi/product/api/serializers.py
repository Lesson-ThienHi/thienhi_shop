from rest_framework import serializers
from ..models import Product, Order, OrderDetails, ProductStatistics

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    size = serializers.CharField(required=True)
    product_type = serializers.CharField(required=True)
    price = serializers.FloatField(required=True)
    unit = serializers.CharField(required=True)
    accessory = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'size', 'price', 'product_type', 'unit', 'accessory')

    def create(self, validated_data):
        product = Product.objects.create(
            name = validated_data['name'],
            size = validated_data['size'],
            product_type = validated_data['product_type'],
            price = validated_data['price'],
            unit = validated_data['unit'],
            accessory = validated_data.get('accessory', None),
        )
        product.save()
        return product


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True)
    order = serializers.IntegerField(required=True)

    class Meta:
        model = OrderDetails
        fields = ['id', 'product', 'quantity', 'order', 'into_money']

    # def create(self, validated_data):
    #     product = Product.objects.get(id=validated_data['product'])
    #     order = Order.objects.filter(id=validated_data['order']).first()
    #     print(product, ' ------------------', order)
    #     if not product:
    #         raise Exception({'errors':'Product Not Found'})
    #     if not order:
    #         raise Exception({'errors':'Order Not Found'})

    #     order_details = OrderDetails(
    #         product = product,
    #         quantity = validated_data['quantity'],
    #         into_money = validated_data['quantity'] * product.price,
    #         order = order,
    #     )
    #     order_details.save()
    #     return order_details


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class UpdateOrderSerializer(serializers.Serializer):
    money_received = serializers.FloatField(required=True)

    class Meta:
        fields = ['money_received']


class ProductStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'