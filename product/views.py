from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view  # type: ignore[reportMissingImports]
from rest_framework.response import Response  # type: ignore[reportMissingImports]
from rest_framework import status  # type: ignore[reportMissingImports]
from .serializers import ProductReviewsSerializer
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, CategoryDetailSerializer,
    ProductSerializer, ProductDetailSerializer,
    ReviewSerializer, ReviewDetailSerializer
)

# CATEGORIES


@api_view(['GET'])
def category_list_api_view(request):
    # step 1: collect categories (QuerySet)
    categories = Category.objects.all()

    # step 2: reformat queryset to list of dictionaries
    list_ = CategorySerializer(categories, many=True).data

    # step 3: return response
    return Response(data=list_)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'category not found!'},
                        status=status.HTTP_404_NOT_FOUND)

    data = CategoryDetailSerializer(category, many=False).data
    return Response(data=data)


# PRODUCTS

@api_view(['GET'])
def product_list_api_view(request):
    # step 1: collect products 
    products = Product.objects.all()

    # step 2: reformat queryset to list of dictionaries 
    list_ = ProductSerializer(products, many=True).data

    # step 3: return response
    return Response(data=list_)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'product not found!'},
                        status=status.HTTP_404_NOT_FOUND)

    data = ProductDetailSerializer(product, many=False).data
    return Response(data=data)


# REVIEWS

@api_view(['GET'])
def review_list_api_view(request):
    # step 1: collect reviews 
    reviews = Review.objects.all()

    # step 2: reformat queryset to list of dictionaries
    list_ = ReviewSerializer(reviews, many=True).data

    # step 3: return response
    return Response(data=list_)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'review not found!'},
                        status=status.HTTP_404_NOT_FOUND)

    data = ReviewDetailSerializer(review, many=False).data
    return Response(data=data)

@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    serializer = ProductReviewsSerializer(products, many=True)
    return Response(data=serializer.data)

