from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from ..models import Customer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    avatar = serializers.ImageField(required=False)
    user_type = serializers.CharField(required=False, default='Staff')
    gender = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'address', 'phone',
            'gender', 'date_of_birth', 'avatar', 'user_type')

    def validate(self, attrs):
        user = User.objects.filter(Q(email=attrs['email']) | Q(username=attrs['email'])).first()
        if user:
            raise serializers.ValidationError({"email": "Email is taken"})

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None),
            phone=validated_data.get('phone', None),
            address=validated_data.get('address', None),
            date_of_birth=validated_data.get('date_of_birth', None),
            avatar=validated_data.get('avatar', None),
            user_type=validated_data.get('user_type'),
            gender=validated_data.get('gender'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


def func_attachment_level(money: float):
    attachment_level = ''
    if money < 1500000:
        attachment_level = 'Level_1'
    elif 1500000 <= money < 9000000:
        attachment_level = 'Level_2'
    elif 9000000 <= money < 25000000:
        attachment_level = 'Level_3'
    elif 25000000 <= money:
        attachment_level = 'Level_4'
    return attachment_level

class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    gender = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    total_money = serializers.FloatField(required=True)

    class Meta:
        model = Customer
        fields = ('name', 'phone', 'gender', 'age', 'total_money', 'attachment_level',)

    def create(self, validated_data):
        customer_is_exit = Customer.objects.filter(phone=validated_data['phone']).first()
        if not customer_is_exit:
            customer = Customer.objects.create(
                name=validated_data['name'],
                phone=validated_data['phone'],
                gender=validated_data['gender'],
                age=validated_data['age'],
                total_money=validated_data['total_money'],
            )
            attachment_level = func_attachment_level(customer.total_money)
            customer.attachment_level = attachment_level
            customer.save()
            return customer
        else:
            customer_is_exit.name = validated_data['name']
            customer_is_exit.gender = validated_data['gender']
            customer_is_exit.age = validated_data['age']
            customer_is_exit.total_money += validated_data['total_money']
            attachment_level = func_attachment_level(customer_is_exit.total_money)

            customer_is_exit.attachment_level = attachment_level
            customer_is_exit.save()
        return customer_is_exit
