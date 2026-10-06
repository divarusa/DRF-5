from rest_framework import serializers  # type: ignore[reportMissingImports]
from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

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

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()  


class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField()


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.01)
    category_id = serializers.IntegerField(min_value=1)

    def validate_category_id(self, category_id):
        if not Category.objects.filter(id=category_id).exists():
            raise serializers.ValidationError("Категория с таким ID не найдена.")
        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=2)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField(min_value=1)

    def validate_product_id(self, product_id):
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError("Товар с таким ID не найден.")
        return product_id


