from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        read_only_fields = ("owner",)
        fields = [
            "id",
            "product_name",
            "model",
            "release_date",
            "owner",
        ]
