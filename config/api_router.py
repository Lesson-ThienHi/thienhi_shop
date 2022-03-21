from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from shop_thienhi.users.api.views import UserViewSet, CustomerViewSet
from shop_thienhi.product.api.views import ProductViewSet, OrderDetailsViewSet, OrderViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("product", ProductViewSet)
router.register("order", OrderViewSet)
router.register("order_detail", OrderDetailsViewSet)
router.register("customer", CustomerViewSet)



app_name = "api"
urlpatterns = router.urls
