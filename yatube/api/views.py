from rest_framework.viewsets import ReadOnlyModelViewSet

from posts.models import Post
from .serializers import PostSerializer


class PostViewSet(ReadOnlyModelViewSet):
    """Реализация CRUD для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
