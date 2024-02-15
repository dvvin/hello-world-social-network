from django.http import HttpResponse
from .models import User

# Create your views here.
def activateemail(request):
    email = request.GET.get('email', '')
    id = request.GET.get('id', '')

    if email and id:
        user = User.objects.get(email=email, id=id)
        user.is_active = True
        user.save()

        return HttpResponse('User activated. Please login.')

    else:
        return HttpResponse('Invalid url')
