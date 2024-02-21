from django.http import JsonResponse
from django.db.models import Q

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from account.models import User, FriendshipRequest
from account.serializers import UserSerializer
from notification.utils import create_notification

from .forms import PostForm, AttachmentForm
from .models import Post, Like, Comment, Trend
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    CommentSerializer,
    TrendSerializer,
)

from datetime import timedelta
from collections import Counter
from django.utils import timezone


@api_view(["GET"])
def post_detail(request, pk):
    user_ids = [request.user.id] + list(
        request.user.friends.values_list("id", flat=True)
    )

    post = Post.objects.filter(
        Q(created_by_id__in=list(user_ids)) | Q(is_private=False)
    ).get(pk=pk)

    context = {"request": request}
    return JsonResponse({"post": PostDetailSerializer(post, context=context).data})


@api_view(["GET"])
def post_list(request):
    user_ids = [request.user.id] + list(
        request.user.friends.values_list("id", flat=True)
    )
    posts = Post.objects.filter(created_by_id__in=user_ids)

    trend = request.GET.get("trend", "")

    if trend:
        pattern = rf"(?:^| )#{trend}\b"
        posts = posts.filter(body__iregex=pattern).filter(is_private=False)

    serializer = PostSerializer(posts, many=True, context={"request": request})
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    if request.user.id != id:
        if request.user not in user.friends.all():
            posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True, context={"request": request})
    user_serializer = UserSerializer(user, context={"request": request})

    friendship_request_status = False

    if request.user in user.friends.all():
        friendship_request_status = False

    existing_request_sent = FriendshipRequest.objects.filter(
        created_for=user, created_by=request.user
    ).exists()

    existing_request_received = FriendshipRequest.objects.filter(
        created_for=request.user, created_by=user
    ).exists()

    if existing_request_sent or existing_request_received:
        friendship_request_status = True

    return JsonResponse(
        {
            "posts": posts_serializer.data,
            "user": user_serializer.data,
            "friendship_request_status": friendship_request_status,
        },
        safe=False,
    )


@api_view(["POST"])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post, context={"request": request})
        return JsonResponse(serializer.data, safe=False)

    else:
        return JsonResponse(form.errors, status=400)


@api_view(["DELETE"])
def post_delete(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({"message": "post deleted"})


@api_view(["POST"])
def post_report(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by.add(request.user)
    post.save()

    return JsonResponse({"message": "post reported"})


@api_view(["POST"])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    like = post.likes.filter(created_by=request.user).first()

    if like:
        post.likes.remove(like)
        post.likes_count = max(post.likes_count - 1, 0)
        post.save()
        message = "like removed"

    else:
        like = Like.objects.create(created_by=request.user)
        post.likes_count += 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, "postlike", post_id=post.id)

        message = "like created"

    return JsonResponse({"message": message})


@api_view(["GET"])
def post_likes(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        likes = post.likes.all()
        users_who_liked = [like.created_by for like in likes]
        serializer = UserSerializer(users_who_liked, many=True)
        return JsonResponse(serializer.data, safe=False)

    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)


@api_view(["POST"])
def post_create_comment(request, pk):
    comment = Comment.objects.create(
        body=request.data.get("body"), created_by=request.user
    )

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count = post.comments_count + 1
    post.save()

    notification = create_notification(request, "postcomment", post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    def extract_hashtags(text, trends):
        for word in text.split():
            if word[0] == "#":
                trends.append(word[1:])

        return trends

    for trend in Trend.objects.all():
        trend.delete()

    trends = []
    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    twenty_four_hours = this_hour - timedelta(hours=24)

    for post in Post.objects.filter(created_at__gte=twenty_four_hours).filter(
        is_private=False
    ):
        extract_hashtags(post.body, trends)

    for trend in Counter(trends).most_common(5):
        Trend.objects.create(hashtag=trend[0], occurences=trend[1])

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def get_liked_posts(request, id):
    user = User.objects.get(pk=id)
    liked_posts = Post.objects.filter(likes__created_by_id=id)
    post_serializer = PostSerializer(liked_posts, many=True, context={"request": request})

    return JsonResponse({
        "posts": post_serializer.data,
        "user": UserSerializer(user).data
    }, safe=False)
