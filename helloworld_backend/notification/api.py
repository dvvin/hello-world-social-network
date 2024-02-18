from .serializers import NotificationSerializer
from .models import Notification

from django.http import JsonResponse
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view(["GET"])
def notifications(request):
    received_notification = request.user.received_notifications.filter(is_read=False)
    serializer = NotificationSerializer(received_notification, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def read_notification(request, pk):
    notification = Notification.objects.filter(created_for=request.user).get(pk=pk)
    notification.is_read = True
    notification.save()

    return JsonResponse({'message': 'notification read'})
