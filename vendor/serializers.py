from django.contrib.auth import get_user_model
from rest_framework import serializers

from home.serializers import CustomUserSerializer
# from store.serializers import ProductCategorySerializer
from vendor.models import Vendor, VendorStore

User = get_user_model()


class UserVendorSerializer(CustomUserSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'mobile_no', 'ip_address',
            'latitude', 'longitude',
        )


class VendorSerializer(serializers.ModelSerializer):
    user = UserVendorSerializer(read_only=True)
    gender_description = serializers.CharField(
        source='get_gender_display',
        read_only=True
    )

    class Meta:
        model = Vendor
        fields = (
            'user', 'id',
            'first_name', 'last_name',
            'gender', 'gender_description',
            'date_of_birth', 'nin_number',
            'bvn', 'verified_date', 'account_name',
            'account_number', 'bank_name'
        )
        read_only_fields = ['nin', 'verified_date', 'bvn']


class VendorStoreSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(many=False)

    class Meta:
        model = VendorStore
        fields = [
            'uid',
            'vendor',
            'image',
            'description',
        ]


class VendorStoreProductSerializer(serializers.ModelSerializer):
    # products = ProductCategorySerializer(many=True)

    class Meta:
        model = VendorStore
        fields = [
            'vendor',
            'products'
        ]
