from django.urls import path
from home import views as home_views

app_name = 'home'

urlpatterns = [
    path(
        'user/address-books/',
        home_views.UserAddressBookListView.as_view(),
        name='list-address-books'
    ),
    # path(
    #     'user/address-books/add/',
    #     home_views.UserAddressBookCreateView.as_view(),
    #     name='create-address-book'
    # )
]
