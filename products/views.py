from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from products.models import Product
from products.serializers import ProductSerializer


class ProductsCreateAPIView(CreateAPIView):
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        product = serializer.save()
        product.owner = self.request.user.employer
        product.save()


class ProductsListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsUpdateAPIView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(owner=self.request.user.employer)
            return queryset
        else:
            return None


class ProductsDestroyAPIView(DestroyAPIView):
    queryset = Product.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(owner=self.request.user.employer)
            return queryset
        else:
            return None
