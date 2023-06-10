import base64

from django.core.files.base import ContentFile
from posts.models import Comment, Post, Group, Follow, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(':base64,')
            ext = format.split('/')[:1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True,
                            default=serializers.CurrentUserDefault())
    following = SlugRelatedField(slug_field='username',
                                 queryset=User.objects.all())

    def create(self, validated_data):
        user = validated_data['user']
        following = validated_data['following']
        follow = Follow.objects.filter(user=user, following=following)
        if user == following:
            raise serializers.ValidationError('Нельзя '
                                              'подписаться на самого себя!')
        elif follow.exists():
            raise serializers.ValidationError('Вы уже подписаны '
                                              'на этого автора!')
        return Follow.objects.create(user=user, following=following)

    class Meta:
        fields = ('user', 'following')
        model = Follow
