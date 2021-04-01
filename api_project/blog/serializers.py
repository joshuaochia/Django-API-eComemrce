from rest_framework import serializers
from . import models


class BlogCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BlogComment
        fields = (
            'id', 'blog', 'profile',
            'comment', 'date_created',
            )
        read_only_fields = ('id', 'blog', 'profile',)


class BlogSerializer(serializers.ModelSerializer):

    comments = BlogCommentSerializer(many=True, read_only=True)

    class Meta:
        model = models.Blog
        fields = (
            'id', 'author', 'title',
            'date_created', 'tags', 'body', 'comments',
        )
        read_only_fields = ('id',)
        lookup_field = 'id'
