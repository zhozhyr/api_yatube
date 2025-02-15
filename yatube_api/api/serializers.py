from rest_framework import serializers
from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',  # Поле, которое будет отображаться
        read_only=True,         # Запретить изменение через API
    )

    class Meta:
        model = Post
        fields = ['id', 'text', 'pub_date', 'author', 'group']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',  # Поле, которое будет отображаться
        read_only=True,        # Запретить изменение через API
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post')
