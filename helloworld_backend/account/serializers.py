from rest_framework import serializers
from .models import User, FriendshipRequest
from post.models import Post

class UserSerializer(serializers.ModelSerializer):
    liked_posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'friends_count', 'posts_count', 'get_avatar', 'liked_posts_count')

    def get_liked_posts_count(self, obj):
        return Post.objects.filter(likes__created_by=obj).count()


class FriendshipRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = FriendshipRequest
        fields = ('id', 'created_by',)
