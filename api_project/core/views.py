from blog.models import BlogComment
from . import serializers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import (
    generics, permissions,
    authentication, mixins, viewsets
    )
from . import models
from rest_framework.response import Response


class CreateUser(viewsets.ViewSet):

    serializer_class = serializers.UserSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            return Response(serializer.data)


class UserToken(ObtainAuthToken):

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = serializers.UserTokenSerializer


class ManagerUserView(generics.RetrieveUpdateAPIView):

    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'slug'

    def get_object(self):
        return self.request.user


class AddressView(viewsets.ModelViewSet, mixins.UpdateModelMixin):

    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserList(viewsets.ReadOnlyModelViewSet):

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerailizer


class CartViewSet(viewsets.ModelViewSet):

    authentication_classes = (authentication.TokenAuthentication, )
    serializer_class = serializers.AddToCartSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):

        user = self.request.user.profiles
        return models.ProfileProductCart.objects.filter(profile=user)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profiles)


class UserBlogCommentViewSet(viewsets.ModelViewSet):

    authentication_classes = (authentication.TokenAuthentication, )
    serializer_class = serializers.UserBlogCommentSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return BlogComment.objects.filter(user=user)
