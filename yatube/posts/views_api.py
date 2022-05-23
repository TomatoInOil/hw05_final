from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializers import PostSerializer


class APIPostList(APIView):
    """Создание нового объекта и чтение всех для модели Post."""

    def get(self, request):
        """Обработка GET запроса."""
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Обработка POST запроса."""
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIPostDetail(APIView):
    """Чтение, изменение и удаление опеределенного объекта для модели Post."""

    def get(self, request, pk):
        """Обработка GET запроса."""
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        """Обработка PUT запроса."""
        post = get_object_or_404(Post, pk=pk)
        serializers = PostSerializer(
            instance=post, data=request.data, partial=True
        )
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        """Обработка PATCH запроса."""
        post = get_object_or_404(Post, pk=pk)
        serializers = PostSerializer(
            instance=post, data=request.data, partial=True
        )
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        """Обработка DELETE запроса."""
        get_object_or_404(Post, pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
