from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели постов."""

    class Meta:
        model = Post
        fields = ('pub_date', 'text', 'image')
