from django.urls import path

from vendor import views as vendor_views

app_name = 'vendor'

urlpatterns = [
    path(
        'vendor/',
        vendor_views.VendorListView.as_view(),
        name=vendor_views.VendorListView.name
    ),
    path(
        'vendor/profile/',
        vendor_views.VendorDetailView.as_view(),
        name=vendor_views.VendorDetailView.name
    )
]
