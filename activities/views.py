from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Activity

def activity_feed(request):
    activities = Activity.objects.filter(user__in=request.user.friends.all()).order_by('-timestamp')
    return render(request, 'activities/feed.html', {'activities': activities})