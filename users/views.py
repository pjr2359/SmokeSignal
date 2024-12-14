from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from activities.forms import ActivityForm
from activities.models import Activity
from django.contrib.auth import get_user_model
from django.contrib import messages

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
        highness_status = request.POST.get('highness_status')
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
    friends = request.user.friends.all()
    return render(request, 'users/profile.html', {
        'activity_form': activity_form,
        'activities': activities,
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
            'activities': activities
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