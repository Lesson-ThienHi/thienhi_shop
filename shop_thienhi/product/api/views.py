from ..models import Product, Order, OrderDetails, ProductStatistics
from .serializers import ProductSerializer, OrderDetailsSerializer, OrderSerializer, UpdateOrderSerializer, ProductStatisticsSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from shop_thienhi.core.redis_cache_product_statistics import get_cached_device_product_statistics


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        permission = ['Stocker', 'Manager']
        if request.user.user_type in permission:
            sz = ProductSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                sz.save()
                return Response(sz.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        permission = ['Stocker', 'Manager']
        if request.user.user_type in permission:
            sz = ProductSerializer(data=request.data)
            if sz.is_valid(raise_exception=True):
                qs = Product.objects.filter(id=pk).first()
                if qs:
                    qs.name = sz.data['name']
                    qs.size = sz.data['size']
                    qs.product_type = sz.data['product_type']
                    qs.price = sz.data['price']
                    qs.unit = sz.data['unit']
                    qs.accessory = sz.data['accessory']
                    qs.save()
                    return Response(sz.data, status=status.HTTP_200_OK)
                return Response({'success': False, 'errors':'NOT_FOUND_PRODUCT'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        permission = ['Stocker', 'Manager']
        if request.user.user_type in permission:
            qs = Product.objects.filter(id=pk).first()
            if qs:
                qs.delete()
                return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
            return Response({'success': False, 'errors':'NOT_FOUND_PRODUCT'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailsViewSet(viewsets.ModelViewSet):
    queryset = OrderDetails.objects.all()
    serializer_class = OrderDetailsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        permission = ['Staff', 'Manager']
        if request.user.user_type in permission:
            sz = OrderDetailsSerializer(data=request.data)
            sz.is_valid(raise_exception=True)
            data = sz.data
            product = Product.objects.filter(id=data['product']).first()
            order = Order.objects.filter(id=data['order']).first()
            if not product:
                raise Exception({'errors':'Product Not Found'})
            if not order:
                raise Exception({'errors':'Order Not Found'})

            order_details = OrderDetails(
                product = product,
                quantity = data['quantity'],
                into_money = data['quantity'] * product.price,
                order = order,
                timestamp = datetime.now().replace(second=0, microsecond=0).timestamp()
            )
            order_details.save()
            response = {
                'id': order_details.id,
                'product': order_details.product.name,
                'quantity': order_details.quantity,
                'order': order_details.order.id,
                'into_money': order_details.into_money,

            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        permission = ['Staff', 'Manager']
        if request.user.user_type in permission:
            sz = OrderDetailsSerializer(data=request.data)
            sz.is_valid(raise_exception=True)
            order_details = OrderDetails.objects.filter(id=pk).first()
            product = Product.objects.filter(id = sz.data['product_id']).first()

            if order_details and product:
                order_details.product = product
                order_details.quantity = sz.data['quantity']
                order_details.into_money = sz.data['into_money']
                order_details.save()
                return Response(sz.data, status=status.HTTP_200_OK)
            elif not order_details:
                return Response({'errors':'Order Not Found'})
            elif not product:
                return Response({'errors':'Product Not Found'})
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        permission = ['Staff', 'Manager']
        if request.user.user_type in permission:
            qs = OrderDetails.objects.filter(id=pk).first()
            if qs:
                qs.delete()
                return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)
            return Response({'success': False, 'errors':'NOT_FOUND_PRODUCT'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None, *args, **kwargs):
        permission = ['Staff', 'Manager']
        if request.user.user_type in permission:
            order = Order.objects.filter(id=pk).first()
            if order:
                order_details = OrderDetails.objects.filter(order=order)
                total = 0
                for i in order_details:
                    total += i.into_money
                data = {
                    'total': total,
                    'created_at': order.created_at,
                    'created_by': order.created_by
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response({'errors':'Order Not Found'})
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        permission = ['Staff', 'Manager']
        if request.user.user_type in permission:
            sz = OrderSerializer(data=request.data)
            sz.is_valid(raise_exception=True)
            qs = Order.objects.create(
                total = 0,
                money_received = 0,
                refunds = 0,
                created_at = datetime.now(),
                created_by = request.user.username,
                timestamp = datetime.now().replace(second=0, microsecond=0).timestamp()
            )
            qs.save()
            data = {
                'total' : qs.total,
                'money_received' : qs.money_received,
                'refunds' : qs.refunds,
                'created_at' : qs.created_at,
                'created_by' : qs.created_by
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        permission = ['Staff', 'Manager']
        if request.user.user_type in permission:
            order = Order.objects.filter(id=pk).first()
            if order:
                sz =UpdateOrderSerializer(data=request.data)
                sz.is_valid(raise_exception=True)
                order_details = OrderDetails.objects.filter(order=order)
                total = 0
                for i in order_details:
                    total += i.into_money
                refunds = sz.data['money_received'] - total
                order.total = total
                order.money_received = sz.data['money_received']
                order.refunds = refunds
                order.save()
                data = {
                    'total' : order.total,
                    'money_received' : order.money_received,
                    'refunds' : order.refunds,
                    'created_at' : order.created_at,
                    'created_by' : order.created_by
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response({'errors':'Order Not Found'})
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=True, url_path="statistic")
    def statistic(self, request, *args, **kwargs):
        
        return Response({'success': False,'errors':'NOT_HAVE_ACCESS'}, status=status.HTTP_400_BAD_REQUEST)


class ProductStatisticsViewSet(viewsets.ModelViewSet):
    queryset = ProductStatistics.objects.all()
    serializer_class = ProductStatisticsSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request,*args, **kwargs):
        data = get_cached_device_product_statistics()
        return Response(data)