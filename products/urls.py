from django.urls import path

from participants.permissions import IsActiveEmployee
from products.apps import ProductsConfig
from products.permissions import IsOwner
from products.views import (ProductsCreateAPIView, ProductsDestroyAPIView,
                            ProductsListAPIView, ProductsRetrieveAPIView,
                            ProductsUpdateAPIView)

app_name = ProductsConfig.name


urlpatterns = [
    path(
        "create/",
        ProductsCreateAPIView.as_view(permission_classes=(IsActiveEmployee,)),
        name="create",
    ),
    path(
        "",
        ProductsListAPIView.as_view(permission_classes=(IsActiveEmployee,)),
        name="list",
    ),
    path(
        "view/<int:pk>/",
        ProductsRetrieveAPIView.as_view(permission_classes=(IsActiveEmployee,)),
        name="view",
    ),
    path(
        "update/<int:pk>/",
        ProductsUpdateAPIView.as_view(permission_classes=(IsOwner,)),
        name="update",
    ),
    path(
        "delete/<int:pk>/",
        ProductsDestroyAPIView.as_view(permission_classes=(IsOwner,)),
        name="delete",
    ),
]
