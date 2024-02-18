from django.db import models
import uuid
from account.models import User
from post.models import Post


class Notification(models.Model):
    NEW_FRIEND_REQUEST = "newfriendrequest"
    ACCEPTED_FRIEND_REQUEST = "acceptedfriendrequest"
    REJECTED_FRIEND_REQUEST = "rejectedfriendrequest"
    POST_LIKE = "postlike"
    POST_COMMENT = "postcomment"

    TYPE_OF_NOTIFICATION = (
        (NEW_FRIEND_REQUEST, "New friend request"),
        (ACCEPTED_FRIEND_REQUEST, "Accepted friend request"),
        (REJECTED_FRIEND_REQUEST, "Rejected friend request"),
        (POST_LIKE, "Post like"),
        (POST_COMMENT, "Post comment"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField()
    is_read = models.BooleanField(default=False)

    notification_type = models.CharField(max_length=50, choices=TYPE_OF_NOTIFICATION)

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)

    created_by = models.ForeignKey(
        User, related_name="created_notifications", on_delete=models.CASCADE
    )
    created_for = models.ForeignKey(
        User, related_name="received_notifications", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
