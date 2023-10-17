from django.urls import path

from store import views as store_views

app_name = "store"

urlpatterns = [
    path(
        "store/product-categories/",
        store_views.ProductCategoryListAPIView.as_view(),
        name='product-categories',
    ),
    path(
        "store/products/",
        store_views.ProductListAPIView.as_view(),
        name='products'
    ),
    path(
        "store/product/<slug:slug>/",
        store_views.ProductDetailAPIView.as_view(),
        name='product'
    ),
    path(
        "",
        store_views.ApiRootView.as_view(),
        name=store_views.ApiRootView.name
    ),

]
