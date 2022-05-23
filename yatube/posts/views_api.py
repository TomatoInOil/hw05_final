from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from .models import Post
from .serializers import PostSerializer


class APIPostList(ListCreateAPIView):
    """Создание нового объекта и чтение всех для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer


class APIPostDetail(RetrieveUpdateDestroyAPIView):
    """Чтение, изменение и удаление опеределенного объекта для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer