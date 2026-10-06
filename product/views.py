from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, CategoryDetailSerializer,
    ProductSerializer, ProductDetailSerializer,
    ReviewSerializer, ReviewDetailSerializer, ProductReviewsSerializer,
    CategoryValidateSerializer, ProductValidateSerializer, ReviewValidateSerializer
)


# CATEGORIES

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        list_ = CategorySerializer(categories, many=True).data
        return Response(data=list_)

    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        name = serializer.validated_data.get('name')
        category = Category.objects.create(name=name)
        return Response(data=CategoryDetailSerializer(category).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'category not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = CategoryDetailSerializer(category, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(data=CategoryDetailSerializer(category).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PRODUCTS 

@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        list_ = ProductSerializer(products, many=True).data
        return Response(data=list_)

    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        product = Product.objects.create(**serializer.validated_data)
        return Response(data=ProductDetailSerializer(product).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ProductDetailSerializer(product, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        for key, value in serializer.validated_data.items():
            setattr(product, key, value)
        product.save()
        return Response(data=ProductDetailSerializer(product).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# REVIEWS 

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        list_ = ReviewSerializer(reviews, many=True).data
        return Response(data=list_)

    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        review = Review.objects.create(**serializer.validated_data)
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'review not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = ReviewDetailSerializer(review, many=False).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

        for key, value in serializer.validated_data.items():
            setattr(review, key, value)
        review.save()
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# PRODUCTS WITH REVIEWS

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    serializer = ProductReviewsSerializer(products, many=True)
    return Response(data=serializer.data)
