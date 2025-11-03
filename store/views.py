from django.http import HttpResponse

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product


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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)

    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)

    # we can use the get_object_or_404 shortcut to simplify this

    # product = get_object_or_404(Product, pk=id)
    # serializer = ProductSerializer(product)
    # return Response(serializer.data)

    if request.method == 'GET':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()  # Save the updated product to the database
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data
        serializer.save()  # Save the updated product to the database
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        product = get_object_or_404(Product, pk=id)
        product.delete()  # Delete the product from the database
        return Response(status=status.HTTP_204_NO_CONTENT)
