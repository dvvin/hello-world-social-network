from django.http import JsonResponse
from .forms import PostForm
from .models import Post, Like
from .serializers import PostSerializer
from account.models import User
from account.serializers import UserSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id] + list(request.user.friends.values_list('id', flat=True))
    posts = Post.objects.filter(created_by_id__in=user_ids)

    serializer = PostSerializer(posts, many=True, context={'request': request})
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    posts_serializer = PostSerializer(posts, many=True, context={'request': request})
    user_serializer = UserSerializer(user, context={'request': request})

    return JsonResponse(
        {"posts": posts_serializer.data, "user": user_serializer.data}, safe=False
    )

@api_view(["POST"])
def post_create(request):
    form = PostForm(request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serializer = PostSerializer(post, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    else:
        return JsonResponse(form.errors, status=400)

@api_view(['POST'])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)
    like = post.likes.filter(created_by=request.user).first()

    if like:
        post.likes.remove(like)
        post.likes_count = max(post.likes_count - 1, 0)
        post.save()
        message = 'like removed'

    else:
        like = Like.objects.create(created_by=request.user)
        post.likes_count += 1
        post.likes.add(like)
        post.save()
        message = 'like created'

    return JsonResponse({'message': message})
