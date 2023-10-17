from django_filters import rest_framework as filters

from store.models import Product


class ProductCategoryFilter(filters.FilterSet):
    category = filters.CharFilter('category__name', lookup_expr='icontains')
    sub_categories = filters.CharFilter('sub_categories__name', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'sub_categories']
