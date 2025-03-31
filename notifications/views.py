from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-timestamp")
    return render(request, "notifications/notifications.html", {"notifications": notifications})
