from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "id",
            "body",
            "notification_type",
            "post_id",
            "created_by",
            "created_for_id",
        )
