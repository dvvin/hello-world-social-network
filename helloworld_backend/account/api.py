from django.http import JsonResponse
from .forms import SignupForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

@api_view(["GET"])
def me(request):
    return JsonResponse(
        {
            "id": request.user.id,
            "name": request.user.name,
            "email": request.user.email,
        }
    )

@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = "success"

    form = SignupForm(
        {
            "email": data.get("email"),
            "name": data.get("name"),
            "password1": data.get("password1"),
            "password2": data.get("password2"),
        }
    )

    if form.is_valid():
        form.save()

    else:
        message = "error"

    return JsonResponse({"message": message, "errors": form.errors})

@api_view(["POST"])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)

    existing_request_sent = FriendshipRequest.objects.filter(
        created_for=user, created_by=request.user
    ).exists()

    existing_request_received = FriendshipRequest.objects.filter(
        created_for=request.user, created_by=user
    ).exists()

    if existing_request_sent or existing_request_received:
        return JsonResponse({"message": "request already sent"})

    else:
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)
        return JsonResponse({"message": "friendship request created"})

@api_view(["GET"])
def friends(request, pk):
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(
            created_for=request.user, status=FriendshipRequest.SENT
        )
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friends = user.friends.all()

    return JsonResponse(
        {
            "user": UserSerializer(user).data,
            "friends": UserSerializer(friends, many=True).data,
            "requests": requests,
        },
        safe=False,
    )

@api_view(["POST"])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(
        created_for=request.user, created_by=user
    ).first()

    if status == "accepted":
        friendship_request.status = status
        friendship_request.save()

        user.friends.add(request.user)
        user.friends_count = user.friends_count + 1
        user.save()

        request_user = request.user
        request_user.friends_count = request_user.friends_count + 1
        request_user.save()

        message = "Friendship request accepted"

    elif status == "rejected":
        friendship_request.delete()
        message = "Friendship request rejected"

    elif status == "sent":
        message = "Friendship request already sent"

    return JsonResponse({"message": message})


@api_view(["POST"])
def editprofile(request):
    user = request.user
    email = request.data.get("email")

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({"message": "Email already in use"})

    else:
        user.email = email
        user.name = request.data.get("name")
        user.save()
        return JsonResponse({"message": "Profile updated"})
