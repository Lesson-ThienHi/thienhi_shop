from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from shop_thienhi.users.api.serializers import RefreshTokenSerializer, MyTokenObtainPairSerializer
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
