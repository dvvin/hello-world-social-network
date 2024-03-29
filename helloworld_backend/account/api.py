from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings

from notification.utils import create_notification
from .forms import SignupForm, ProfileForm
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
            "avatar": request.user.get_avatar(),
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
        user = form.save()
        user.is_active = False
        user.save()

        url = f"{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}"

        send_mail(
            "Please verify your email",
            f"The url for activating your account is: {url}",
            "noreply@helloworld.com",
            [user.email],
            fail_silently=False,
        )

    else:
        message = form.errors.as_json()

    return JsonResponse({"message": message}, safe=False)


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
        friendrequest = FriendshipRequest.objects.create(
            created_for=user, created_by=request.user
        )
        notification = create_notification(
            request, "newfriendrequest", friendrequest_id=friendrequest.id
        )

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

        notification = create_notification(
            request, "acceptedfriendrequest", friendrequest_id=friendship_request.id
        )

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
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)

        return JsonResponse({"message": "Profile updated", "user": serializer.data})


@api_view(["POST"])
def editpassword(request):
    user = request.user

    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()
        return JsonResponse({"message": "success"})

    else:
        return JsonResponse({"message": form.errors.as_json()}, safe=False)

@api_view(["GET"])
def my_friendship_suggestions(request):
    serializer = UserSerializer(request.user.people_you_may_know.all(), many=True)

    users = User.objects.all()

    for user in users:
        user.people_you_may_know.clear()

        for friend in user.friends.all():
            for friend_of_friend in friend.friends.all():
                if friend_of_friend not in user.friends.all() and friend_of_friend != user:
                    user.people_you_may_know.add(friend_of_friend)

    return JsonResponse(serializer.data, safe=False)
