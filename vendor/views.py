from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from vendor.models import Vendor
from vendor.serializers import VendorSerializer
from home.custom_permissions import IsOwnerOrReadOnly


class VendorListView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    name = 'vendor-list'

    def get_queryset(self):
        qs = Vendor.objects.select_related('user')
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    name = 'vendor-detail'

    def get_object(self):
        qs = Vendor.objects.select_related('user')\
            .get(user=self.request.user)
        return qs

    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)
