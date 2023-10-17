from rest_framework import serializers

from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import extend_schema_serializer

from store.models import Category, Product, ProductImage, SubCategory


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = [
            "name",
        ]
        read_only_fields = ["slug"]


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
            "sub_categories",
        )
        read_only_fields = ["slug"]


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            "image",
        ]


class ProductSerializer(serializers.ModelSerializer):
    vendor_store = serializers.StringRelatedField(many=False, read_only=True)
    product_images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "vendor_store",
            "name",
            "slug",
            "price",
            "image",
            "product_images",
            "in_stock",
            "quantity",
            "description",
            "specification",
        ]
        read_only_fields = ["slug"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        product_images = data.pop("product_images")
        images = [image["image"] for image in product_images]
        data.update({
            "product_images": images,
        })

        return data


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Product Category Endpoint',
            summary='short summary',
            description=(
                'Api endpoint for product category, you can filter by category' +
                'and subcategory by passing query parameters'
            ),
            value={
                "name": "Nike Airforce 1",
                "slug": "nike-airforce-1",
                "image": "http://localhost:8000/uploads/images/product/airmax.jpeg",
                "price": "49000.00",
                "category": "Fashion",
                "sub_categories": [
                    "Shoe",
                    "Sneakers"
                ]
            },
            # request_only=True,  # signal that example only applies to requests
            # response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class ProductCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "name",
            "slug",
            "image",
            "price",
            "category",
            "sub_categories",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        sub_categories = data.pop("sub_categories")
        sub_categories_list = [sub_category["name"] for sub_category in sub_categories]
        data.update({
            "sub_categories": sub_categories_list,
        })

        return data
