from rest_framework import viewsets, permissions, authentication
from . import models, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter


class BaseAttrViewSet(viewsets.ModelViewSet):

    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'id'


class CategoryView(BaseAttrViewSet):

    """
    Viewing all of the category and the products filtered to it.
    """

    queryset = models.Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer


class ProductsListView(BaseAttrViewSet):

    """ Listing all of the products with retrieve, update, and delete method.
        Also have a function to add a variant of a product,
        add images to variant, add tags to product, add a review to product.
    """
    serializer_class = serializers.ProductListSerializer
    queryset = models.Product.objects.all()

    search_fields = ('name', 'category__name')
    filter_backends = (SearchFilter,)

    def get_queryset(self):
        """ Filtering of tags"""

        tags = self.request.query_params.get('tags')
        queryset = self.queryset

        if tags:
            return queryset.filter(tags__tag=tags)

        return models.Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'variant':
            return serializers.VariantProductSerializer
        if self.action == 'image':
            return serializers.ProductImageSerializer
        if self.action == 'tag':
            return serializers.ProductTagSerializer

        return self.serializer_class

    @action(
        methods=['POST', 'GET', 'DELETE', 'PATCH'],
        detail=True, url_path='variant'
        )
    def variant(self, request, id=None):
        """ Upload a variant to a product """

        product = self.get_object()
        variant = models.ProductVariant.objects.filter(product=product)
        serializer = self.get_serializer(
            variant, many=True,
        )

        # Filtering a specific variant using Get
        variant_id = self.request.query_params.get('id')

        if variant_id:
            var = variant.get(id=int(variant_id))
            serializer = self.get_serializer(var)
            if request.method == 'DELETE':
                var.delete()
            return Response(serializer.data)
        # Filtering Using Get

        # Deleting all the variant
        if request.method == 'DELETE':
            variant.delete()

        # Editing all variant
        if request.method == 'PATCH':
            serializer = self.get_serializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        # Posting new variant
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(product=product)
                return Response(serializer.data)

        return Response(serializer.data)

    @action(methods=['POST', 'GET', 'DELETE'], detail=True, url_path='image')
    def image(self, request, id=None):
        """ Upload an image to a specific product variant """

        query = models.ProductImage.objects.all()

        serializer = self.get_serializer(query, many=True)
        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                )

        return Response(serializer.data)

    @action(methods=['POST', 'GET', 'DELETE'], detail=True, url_path='tag')
    def tag(self, request, id=None):
        """ Upload a tag for product """

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(product=self.get_object())
            return Response(serializer.data)

        return Response(serializer.data)


class ProductReviewApi(viewsets.ModelViewSet):

    serializer_class = serializers.ProductReviewSerializer

    def get_queryset(self):
        user = self.request.user
        return models.ProductReview.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)
