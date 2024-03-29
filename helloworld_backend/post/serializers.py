from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Post, Comment, Trend, PostAttachment


class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAttachment
        fields = ("id", "get_image")


class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "created_by",
            "created_at_formatted",
            "likes_count",
            "is_liked_by_user",
            "comments_count",
            "attachments",
            "is_private",
        )

    def get_is_liked_by_user(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return obj.likes.filter(created_by=request.user).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "body",
            "created_by",
            "created_at_formatted",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    is_liked_by_user = serializers.SerializerMethodField()
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "body",
            "likes_count",
            "comments_count",
            "created_by",
            "created_at_formatted",
            "comments",
            "is_liked_by_user",
            "attachments",
        )

    def get_is_liked_by_user(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return obj.likes.filter(created_by=request.user).exists()
        return False


class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = (
            "id",
            "hashtag",
            "occurences",
        )
