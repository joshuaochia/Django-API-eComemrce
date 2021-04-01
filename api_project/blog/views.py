from rest_framework import viewsets, permissions
from . import models, serializers
from rest_framework.decorators import action
from rest_framework.response import Response


class BlogApiView(viewsets.ModelViewSet):

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    serializer_class = serializers.BlogSerializer
    queryset = models.Blog.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.action == 'comment':
            return serializers.BlogCommentSerializer

        return self.serializer_class

    @action(methods=['POST', 'GET', 'DELETE'], detail=True, url_path='comment')
    def comment(self, request, id=None):

        obj = self.get_object()
        user = self.request.user.profiles

        query = models.BlogComment.objects.filter(blog=obj, profile=user)

        serializer = self.get_serializer(query, many=True)

        if request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():

                serializer.save(
                    blog=obj,
                    profile=user
                )
                return Response(serializer.data)

        return Response(serializer.data)
