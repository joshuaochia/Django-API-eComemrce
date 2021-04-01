from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from . import models
from blog.models import BlogComment


class HelloSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
                'password': {
                    'write_only':
                        'True',
                    'style':
                        {'input_type': 'password'}
                            }
                        }

    def create(self, validated_data):
        """ Create a new user with encrypted password and return it """
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """ Update user and set the password correctly """

        password = validated_data.pop('password')
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return password


class ProfileSerailizer(serializers.ModelSerializer):

    class Meta:
        model = models.Profile
        fields = ('profile', 'full_name', 'slug')
        lookup_field = 'slug'


class UserTokenSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                                            'Wrong info kid!',
                                            code='authentication'
                                            )

        attrs['user'] = user

        return attrs


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        fields = ('street_address', 'apartment_address', 'country', 'zip_code')


class AddToCartSerializer(serializers.ModelSerializer):
    """ Add a specific product to the user cart """

    class Meta:
        model = models.ProfileProductCart
        fields = ('id', 'profile', 'product', 'cost', 'quantity')
        read_only_fields = ('profile', 'id')


class UserBlogCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogComment
        fields = ('id', 'blog', 'user', 'comment')
        read_only_fields = ('id', 'blog', 'user',)
