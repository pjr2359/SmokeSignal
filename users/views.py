from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from activities.forms import ActivityForm
from activities.models import Activity
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import CustomUser, FriendRequest
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')  # Redirect to 'profile' after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def update_status(request):
    if request.method == 'POST':
        highness_status = request.POST.get('highness_status')
        request.user.highness_status = highness_status
        request.user.save()
        return redirect('profile')
    return render(request, 'users/update_status.html')

@login_required
def profile(request):
    if request.method == 'POST':
        # Update highness status
        print("The request post is: " + request.POST )  # Debugging 
        highness_status = request.POST.get('highness_status')
        if highness_status is not None:
            print("The highness status is: " + highness_status)  # Debugging
        else:
            print("The highness status is None")
        if highness_status is not None:
            request.user.highness_status = highness_status
            request.user.save()
        
        # Log activity
        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('profile')
    else:
        activity_form = ActivityForm()
    
    activities = Activity.objects.filter(user=request.user).order_by('-timestamp')
    sent_requests = FriendRequest.objects.filter(from_user=request.user, accepted=False)
    received_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    friends = CustomUser.objects.filter(
        sent_friend_requests__to_user=request.user,
        sent_friend_requests__accepted=True
    ) | CustomUser.objects.filter(
        received_friend_requests__from_user=request.user,
        received_friend_requests__accepted=True
    )
    return render(request, 'users/profile.html', {
        'activity_form': activity_form,
        'activities': activities,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
        'friends': friends,
    })

@login_required
def add_friend(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            friend = User.objects.get(username=username)
            request.user.friends.add(friend)
            messages.success(request, f'You are now friends with {friend.username}')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        return redirect('profile')

@login_required
def view_profile(request, username):
    try:
        profile_user = User.objects.get(username=username)
        activities = Activity.objects.filter(user=profile_user).order_by('-timestamp')
        return render(request, 'users/view_profile.html', {
            'profile_user': profile_user,
            'activities': activities,
            'request_location': True  # Flag to enable location request
        })
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('profile')

def home(request):
    return render(request, 'users/home.html')

@login_required
def log_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('profile')
    else:
        form = ActivityForm()
    return render(request, 'users/log_activity.html', {'form': form})

@login_required
def send_friend_request(request, username):
    if request.user.username == username:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('profile')
        
    try:
        to_user = CustomUser.objects.get(username=username)
        if FriendRequest.objects.filter(from_user=request.user, to_user=to_user, accepted=False).exists():
            messages.info(request, f'Friend request already sent to {to_user.username}')
        else:
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            messages.success(request, f'Friend request sent to {to_user.username}')
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
    return redirect('profile')

@login_required
def accept_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id)
        if friend_request.to_user == request.user:
            friend_request.accepted = True
            friend_request.save()
            messages.success(request, f'You are now friends with {friend_request.from_user.username}')
        else:
            messages.error(request, 'You are not authorized to accept this friend request.')
    except FriendRequest.DoesNotExist:
        messages.error(request, 'Friend request not found.')
    return redirect('profile')

@login_required
def activity_map(request):
    return render(request, 'users/activity_map.html')

@login_required
def friend_activities_api(request):
    friends = CustomUser.objects.filter(
        Q(sent_friend_requests__to_user=request.user, sent_friend_requests__accepted=True) |
        Q(received_friend_requests__from_user=request.user, received_friend_requests__accepted=True)
    ).distinct()
    
    activities = Activity.objects.filter(
        user__in=friends,
        latitude__isnull=False,
        longitude__isnull=False
    ).order_by('-timestamp')
    
    print(f"Found {activities.count()} activities for user {request.user.username}")
    print(f"Friends: {[f.username for f in friends]}")
    
    data = [{
        'user': activity.user.username,
        'strain_name': activity.strain_name,
        'strain_type': activity.strain_type,
        'rating': activity.rating,
        'location': activity.location,
        'latitude': float(activity.latitude),
        'longitude': float(activity.longitude),
        'timestamp': activity.timestamp.isoformat()
    } for activity in activities]
    
    print(f"Returning {len(data)} activities")
    return JsonResponse(data, safe=False)