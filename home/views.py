from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# from home.custom_permissions import IsOwnerOrReadOnly
from home.models import AddressBook
from home.serializers import (
    UserAddressBookSerializer
)


class UserAddressBookListView(generics.ListCreateAPIView):
    serializer_class = UserAddressBookSerializer
    permission_classes = [IsAuthenticated]
    queryset = AddressBook.objects.all()

    def get_queryset(self):
        qs = AddressBook.objects.select_related('user')\
            .filter(user=self.request.user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class UserAddressBookCreateView(generics.CreateAPIView):
#     serializer_class = AddressBookSerializer
#     permission_classes = [IsAuthenticated | IsOwner]
