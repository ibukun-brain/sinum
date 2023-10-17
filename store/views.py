from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from store import serializers
from store.filters import ProductCategoryFilter
from store.models import Product


class ProductCategoryListAPIView(generics.ListAPIView):
    """
    API endpoint for getting all product categories
    """
    serializer_class = serializers.ProductCategorySerializer
    filterset_class = ProductCategoryFilter
    name = "Product Categories"

    def get_queryset(self):
        qs = Product.items.select_related(
            'category',
        ).prefetch_related('sub_categories').all()
        return qs


class ProductListAPIView(generics.ListAPIView):
    """
    API endpoint for getting all products
    """
    serializer_class = serializers.ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    name = "Products"

    def get_queryset(self):
        qs = Product.items.select_related(
            'category',
            'vendor_store',
            'vendor_store__vendor',
            'vendor_store__vendor__user'
        ).prefetch_related('sub_categories', 'product_images').all()
        return qs


class ProductDetailAPIView(generics.RetrieveAPIView):
    """
    Api endpoint for getting a single product
    """
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    name = 'Product'


class ApiRootView(generics.GenericAPIView):
    name = 'ApiRoot'

    def get(self, request, *args, **kwargs):
        return Response({
            'products-categories': reverse(
                "store:product-categories",
                request=request
            ),
            'products': reverse("store:products", request=request),
        })
