from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from activities.forms import ActivityForm
from activities.models import Activity

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def update_highness_status(request):
    if request.method == 'POST':
        highness_status = request.POST.get('highness_status')
        request.user.highness_status = highness_status
        request.user.save()
        return redirect('profile')
    return render(request, 'users/update_highness_status.html')

@login_required
def profile(request):
    if request.method == 'POST':
        activity_form = ActivityForm(request.POST)
        if activity_form.is_valid():
            activity = activity_form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('profile')
        else:
            activity_form = ActivityForm()

        activities = Activity.objects.filter(user=request.user).order_by('-timestamp')

        return render(request, 'users/profile.html', {'activity_form': activity_form, 'activities': activities})


def home(request):
    return render(request, 'users/home.html')