from django.contrib.auth import get_user_model
from django_user_agents.utils import get_user_agent

from djoser.serializers import (
    UserCreateSerializer, UserSerializer
)

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from rest_framework import serializers

from home.models import AddressBook

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = (
            'email', 'password',
        )


class CustomUserSerializer(UserSerializer):
    """
    Using django user agent package we can get the user device
    and serialize the data
    """
    user_device = serializers.SerializerMethodField(
        method_name='get_user_device'
    )

    @extend_schema_field(OpenApiTypes.STR)
    def get_user_device(self, obj):
        request = self.context.get('request')
        user_agent = get_user_agent(request)
        return user_agent.os.family

    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email',
            'mobile_no', 'ip_address',
            'latitude', 'longitude',
            'user_device'
        )


class UserAddressBookSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    phone_no = serializers.CharField(source='user.mobile_no')

    class Meta:
        model = AddressBook
        fields = (
            'user', 'first_name', 'last_name',
            'phone_no', 'additional_phone_no',
            'delivery_address', 'default_address',
            'state', 'city', 'town'
        )


# class UserAddressBookSerializer(serializers.ModelSerializer):
#     user = CustomUserCreateSerializer()

#     class Meta:
#         model = AddressBook
#         fields = (
#             'user', 'phone_no', 'additional_phone_no',
#             'delivery_address', 'default_address',
#             'state', 'city', 'town'
#         )
