from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from posts.models import Group, Post
from .serializers import PostSerializer, GroupSerializer


class PostViewSet(ModelViewSet):
    """Реализация CRUD для модели Post."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer

class GroupViewSet(ReadOnlyModelViewSet):
    """Реализация чтения для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer