from decimal import Decimal
from rest_framework import serializers

from store.models import Product, Review


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=200)
#     # price_without_tax = serializers.DecimalField(
#     #     max_digits=10, decimal_places=2, source='price')

#     price = serializers.DecimalField(
#         max_digits=10, decimal_places=2,)
#     price_with_tax = serializers.SerializerMethodField(
#         method_name='calculate_tax')

#     # serializing relationships - primary key
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Product.objects.all()
#     # )

#     # serializing relationships - nested serializer
#     collection = CollectionSerializer()

#     def calculate_tax(self, product: Product) -> Decimal:
#         return product.price * Decimal("1.2")


# Model serializers automatically generate fields based on model attributes
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'collection', 'inventory']
        # fields = '__all__'  # Include all fields from the model

    # Custom field for unit price, mapping to the model's 'price' field
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source='price')

    # Serializing relationships - primary key
    # collection = CollectionSerializer()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'name', 'description', 'date', 'product']
