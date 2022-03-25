from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from shop_thienhi.users.api.views import UserViewSet, CustomerViewSet
from shop_thienhi.product.api.views import ProductViewSet, OrderDetailsViewSet, OrderViewSet, ProductStatisticsViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("product", ProductViewSet)
router.register("order", OrderViewSet)
router.register("order_detail", OrderDetailsViewSet)
router.register("customer", CustomerViewSet)
router.register("product-statistic", ProductStatisticsViewSet)



app_name = "api"
urlpatterns = router.urls
