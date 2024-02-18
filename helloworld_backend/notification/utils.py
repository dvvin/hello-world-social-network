from .models import Notification
from post.models import Post
from account.models import FriendshipRequest


def create_notification(
    request, notification_type, post_id=None, friendrequest_id=None
):
    created_for = None

    if notification_type == "postlike":
        body = f"{request.user.name} liked your post"
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif notification_type == "postcomment":
        body = f"{request.user.name} commented on your post"
        post = Post.objects.get(pk=post_id)
        created_for = post.created_by

    elif notification_type == "newfriendrequest":
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_for
        body = f"{request.user.name} sent you a friend request"

    elif notification_type == "acceptedfriendrequest":
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_by
        body = f"{request.user.name} accepted your friend request"

    elif notification_type == "rejectedfriendrequest":
        friendrequest = FriendshipRequest.objects.get(pk=friendrequest_id)
        created_for = friendrequest.created_by
        body = f"{request.user.name} rejected your friend request"

    notification = Notification.objects.create(
        body=body,
        notification_type=notification_type,
        created_by=request.user,
        post_id=post_id,
        created_for=created_for,
    )

    return notification
