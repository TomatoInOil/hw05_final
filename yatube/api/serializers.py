from rest_framework import serializers

from posts.models import Group, Post, Tag, TagPost


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag."""

    class Meta:
        model = Tag
        fields = ('name',)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели постов."""

    group = serializers.SlugRelatedField(
        queryset=Group.objects.all(), required=False, slug_field='slug'
    )
    tag = TagSerializer(many=True, required=False)
    character_quantity = serializers.SerializerMethodField()
    publication_date = serializers.DateTimeField(
        read_only=True, source='pub_date'
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'image',
            'author',
            'publication_date',
            'group',
            'tag',
            'character_quantity',
        )

    def get_character_quantity(self, obj: Post):
        """Вычисление количества символов в посте."""
        all_characters = len(obj.text)
        without_spaces = all_characters - obj.text.count(" ")
        return {
            'all_characters': all_characters,
            'without_spaces': without_spaces,
        }

    def create(self, validated_data: dict):
        """Создание с возможностью изменения группы."""
        received_group = validated_data.pop('group', None)
        received_tags = validated_data.pop('tag', None)
        post: Post = Post.objects.create(**validated_data)

        if not received_group and not received_tags:
            return post

        for tag in received_tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            TagPost.objects.create(tag=current_tag, post=post)

        if received_group:
            post.group = received_group
            post.save()

        return post

    def update(self, instance: Post, validated_data: dict):
        """Обновление с возможностью изменения группы поста."""
        instance.text = validated_data.get('text', instance.text)
        instance.group = validated_data.get('group', instance.group)

        received_tags: list[dict] = validated_data.get('tag', [])
        if received_tags:
            instance_tags = instance.tag.all()
            for instance_tag in instance_tags:
                instance_tag.delete()
            for tag in received_tags:
                current_tag, status = Tag.objects.get_or_create(**tag)
                TagPost.objects.create(tag=current_tag, post=instance)

        instance.save()

        return instance


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = ('slug', 'title', 'description')
