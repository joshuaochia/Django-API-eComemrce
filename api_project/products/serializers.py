from rest_framework import serializers
from .models import (
    Categories, Product,
    ProductVariant, ProductImage,
    ProductReview, ProductTag
    )


class ProductReviewSerializer(serializers.ModelSerializer):

    """ Creating customer review for a certain product"""

    class Meta:
        model = ProductReview
        fields = ('id', 'product', 'star', 'rv_img', 'review', )
        read_only_fields = ('id',)


class ProductTagSerializer(serializers.ModelSerializer):

    """ Serializer for creating tags on products """

    class Meta:
        model = ProductTag
        fields = ('id', 'tag', 'product')
        read_only_fields = ('product', 'id')


class ProductImageSerializer(serializers.ModelSerializer):

    """ Serializer for setting image on specific product Variant"""

    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product_variant')
        read_only_fields = ('id',)


class VariantProductSerializer(serializers.ModelSerializer):

    """ Serializer for creating new variant for a product"""

    img = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = (
            'id', 'name', 'specification',
            'stock', 'product',  'price', 'img'
        )
        read_only_fields = ('id', 'product')
        lookup_field = 'id'
        depth = 2

    def create(self, validated_data):
        images_data = validated_data.pop('img')
        variant = ProductVariant.objects.create(**validated_data)

        # for image in images_data:
        ProductImage.objects.create(product_variant=variant, **images_data)
        return variant


class ProductListSerializer(serializers.ModelSerializer):

    """ Listing all of the products available """
    tags = ProductTagSerializer(many=True, read_only=True)
    variants = VariantProductSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name',
            'description', 'time_posted',
            'category', 'slug', 'tags', 'variants',
            'reviews'
            )

        lookup_field = 'slug'
        read_only_fields = ('id', 'slug')
        # depth = 5


class CategoriesSerializer(serializers.ModelSerializer):

    """ Filtering products from each category """

    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ('id', 'slug', 'name', 'products')
        lookup_field = 'id'
        read_only_fields = ('id', 'slug')
