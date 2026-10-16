from rest_framework import serializers  # type: ignore[reportMissingImports]
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if price <= 0:
            raise serializers.ValidationError("Цена должна быть больше 0.")
        return price


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_text(self, text):
        if len(text.strip()) < 2:
            raise serializers.ValidationError("Текст отзыва слишком короткий.")
        return text


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'reviews', 'rating']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_stars = sum([review.stars for review in reviews])
            return round(total_stars / reviews.count(), 2)
        return 0.0
