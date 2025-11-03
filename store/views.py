from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .serializers import ProductSerializer, ReviewSerializer
from .models import Product, Review
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.viewsets import ModelViewSet


# def product_list(request):
#     return HttpResponse("Product List Page")


# @api_view()
# def product_list(request):
#     queryset = Product.objects.all()
#     serializer = ProductSerializer(queryset, many=True)
#     return Response(serializer.data)


@api_view(['GET', 'POST'])
def product_list(request):

    if request.method == 'GET':
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('Ok')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # we can also use raise_exception=True to automatically return 400 if invalid
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()  # Save the new product to the database
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def product_detail(request, id):
#     # try:
#     #     product = Product.objects.get(pk=id)
#     #     serializer = ProductSerializer(product)

#     #     return Response(serializer.data)
#     # except Product.DoesNotExist:
#     #     return Response(status=status.HTTP_404_NOT_FOUND)

#     # we can use the get_object_or_404 shortcut to simplify this

#     # product = get_object_or_404(Product, pk=id)
#     # serializer = ProductSerializer(product)
#     # return Response(serializer.data)

#     if request.method == 'GET':
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()  # Save the updated product to the database
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'PATCH':
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(
#             product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data
#         serializer.save()  # Save the updated product to the database
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         product = get_object_or_404(Product, pk=id)
#         product.delete()  # Delete the product from the database
#         return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------
# Class Based View

class ProductDetailsView(APIView):

    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()  # Save the new product to the database
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()  # Save the updated product to the database
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()  # Save the updated product to the database
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        product.delete()  # Delete the product from the database
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------
# Mixin Based Views (More DRY approach)
# HOW IT WORKS:
# 1. Request comes in: GET /products/5/
# 2. Django routes to ProductDetailView.as_view()
# 3. DRF calls your get() method
# 4. You call self.retrieve() (from RetrieveModelMixin)
# 5. retrieve() calls self.get_object() (from GenericAPIView)
# 6. get_object() queries Product.objects.all().get(pk=5)
# 7. retrieve() calls self.get_serializer(product)
# 8. Serializer converts product to JSON
# 9. retrieve() returns Response(serialized_data)

class ProductListView(GenericAPIView, ListModelMixin, CreateModelMixin):
    """
    GET - List all products
    POST - Create a new product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# GET - Retrieve a single product
    # PUT - Update entire product
    # PATCH - Partial update
    # DELETE - Delete product

    # COMPARISON: What mixins replace
    # ================================

    # Manual code (ProductDetailsView above):
    #     def get(self, request, id):
    #         product = get_object_or_404(Product, pk=id)  # Manual lookup
    #         serializer = ProductSerializer(product)       # Manual serialization
    #         return Response(serializer.data)              # Manual response

    # With RetrieveModelMixin:
    #     def get(self, request, *args, **kwargs):
    #         return self.retrieve(request, *args, **kwargs)  # Mixin does everything!

    #     # Behind the scenes, retrieve() does:
    #     # - self.get_object() → Product.objects.all().get(pk=kwargs['pk'])
    #     # - self.get_serializer(instance) → ProductSerializer(product)
    #     # - return Response(serializer.data)

    # The mixin methods you're calling:
    # - self.list() → List all products (ListModelMixin)
    # - self.create() → Create new product (CreateModelMixin)
    # - self.retrieve() → Get single product (RetrieveModelMixin)
    # - self.update() → Full update (UpdateModelMixin)
    # - self.partial_update() → Partial update (UpdateModelMixin)
    # - self.destroy() → Delete product (DestroyModelMixin)


class ProductDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'  # Uses 'pk' by default

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# ================================================================================
# ViewSet-Based Views (Most DRY approach)
# ================================================================================
#
# HOW VIEWSETS WORK:
# ------------------
# 1. ViewSet = ONE class for ALL CRUD operations
# 2. Router automatically creates URLs
# 3. No need to manually define HTTP methods (get, post, put, etc.)
#
# COMPARISON OF ALL APPROACHES:
# ------------------------------
# Function-based view:
#   - product_list() = 19 lines
#   - product_detail() = 40 lines
#   - Total: ~59 lines + manual URL routing
#
# Class-based view (APIView):
#   - ProductDetailsView = 35 lines
#   - Total: 35 lines + manual URL routing
#
# Mixin-based views:
#   - ProductListView = 10 lines
#   - ProductDetailView = 17 lines
#   - Total: 27 lines + manual URL routing
#
# ViewSet (below):
#   - ProductViewSet = 3 lines (just queryset + serializer!)
#   - URLs auto-generated by router
#   - Total: 3 lines!
#
# WHAT MODELVIEWSET PROVIDES:
# ----------------------------
# ModelViewSet = GenericViewSet + ALL 5 mixins
#
# Inherits from:
#   - ListModelMixin → list() → GET /products/
#   - CreateModelMixin → create() → POST /products/
#   - RetrieveModelMixin → retrieve() → GET /products/5/
#   - UpdateModelMixin → update() + partial_update() → PUT/PATCH /products/5/
#   - DestroyModelMixin → destroy() → DELETE /products/5/
#
# The Router handles mapping:
#   HTTP Method + URL → ViewSet action
#   GET    /products/          → ProductViewSet.list(request)
#   POST   /products/          → ProductViewSet.create(request)
#   GET    /products/5/        → ProductViewSet.retrieve(request, pk=5)
#   PUT    /products/5/        → ProductViewSet.update(request, pk=5)
#   PATCH  /products/5/        → ProductViewSet.partial_update(request, pk=5)
#   DELETE /products/5/        → ProductViewSet.destroy(request, pk=5)

class ProductViewSet(ModelViewSet):
    """
    A complete ViewSet for Product CRUD operations.

    This single class replaces ProductListView + ProductDetailView!

    Automatically provides:
    - list: GET /products/ → All products
    - create: POST /products/ → Create new product
    - retrieve: GET /products/{id}/ → Single product
    - update: PUT /products/{id}/ → Full update
    - partial_update: PATCH /products/{id}/ → Partial update
    - destroy: DELETE /products/{id}/ → Delete product
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    # if i want to filter by collection_id
    # i.e. GET /products/?collection_id=1
    filterset_fields = ['collection_id',]

    # That's it! Just 2 lines of config and you get full CRUD!

    # ============================================================================
    # OPTIONAL: Override methods for custom behavior
    # ============================================================================

    # def list(self, request, *args, **kwargs):
    #     """Override to add custom list logic"""
    #     print("Listing all products")
    #     return super().list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     """Override to add custom create logic"""
    #     print("Creating a new product")
    #     return super().create(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     """Override to add custom retrieve logic"""
    #     print(f"Retrieving product {kwargs.get('pk')}")
    #     return super().retrieve(request, *args, **kwargs)

    # ============================================================================
    # CUSTOM ACTIONS: Add extra endpoints
    # ============================================================================

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Custom endpoint: GET /products/recent/

        The @action decorator creates a new route.
        - detail=False → Collection endpoint (no id required)
        - methods=['get'] → Only GET requests allowed

        Returns the 5 most recently created products
        """
        recent_products = Product.objects.all().order_by('-id')[:5]
        serializer = self.get_serializer(recent_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def discount(self, request, pk=None):
        """
        Custom endpoint: POST /products/{id}/discount/

        The @action decorator creates a new route.
        - detail=True → Detail endpoint (requires id)
        - methods=['post'] → Only POST requests allowed

        Apply a discount to a specific product
        """
        product = self.get_object()
        discount_percent = request.data.get('percent', 10)
        # Custom discount logic would go here
        return Response({
            'status': 'success',
            'message': f'{discount_percent}% discount applied to {product.title}'
        })


class ReviewViewSet(ModelViewSet):
    """
    A complete ViewSet for Review CRUD operations.

    Automatically provides:
    - list: GET /reviews/ → All reviews
    - create: POST /reviews/ → Create new review
    - retrieve: GET /reviews/{id}/ → Single review
    - update: PUT /reviews/{id}/ → Full update
    - partial_update: PATCH /reviews/{id}/ → Partial update
    - destroy: DELETE /reviews/{id}/ → Delete review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
