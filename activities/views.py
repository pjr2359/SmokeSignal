from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from activities.models import Activity
from django.contrib.auth import get_user_model

from django.db.models import Q
from .models import Activity
from .services import GDELTNewsService



def activity_feed(request):
    activities = Activity.objects.filter(user__in=request.user.friends.all()).order_by('-timestamp')
    return render(request, 'activities/feed.html', {'activities': activities})

@login_required
def main_feed(request):
    friends = CustomUser.objects.filter(
        Q(sent_friend_requests__to_user=request.user, sent_friend_requests__accepted=True) |
        Q(received_friend_requests__from_user=request.user, received_friend_requests__accepted=True)
    ).distinct()
    
    activities = Activity.objects.filter(
        Q(user__in=friends) | Q(user=request.user)
    ).order_by('-timestamp')

    news_articles = GDELTNewsService.get_cannabis_news()
    return render(request, 'activities/main_feed.html', {
        'activities': activities,
        'news_articles': news_articles
})