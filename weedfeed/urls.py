"""weedfeed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from activities import views as activity_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('update_highness_status/', user_views.update_highness_status, name='update_highness_status'),
    path('feed/', activity_views.activity_feed, name='feed'),
    path('profile/', user_views.profile, name='profile'),
    path('update_status/', user_views.update_status, name='update_status'),
    path('add_friend/', user_views.add_friend, name='add_friend'),
    path('user/<str:username>/', user_views.view_profile, name='view_profile'),
    path('send_friend_request/', user_views.send_friend_request, name='send_friend_request'),
    path('send_friend_request/<str:username>/', user_views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:request_id>/', user_views.accept_friend_request, name='accept_friend_request'),
    path('log_activity/', user_views.log_activity, name='log_activity'),
    path('activity-map/', user_views.activity_map, name='activity_map'),
    path('api/friend-activities/', user_views.friend_activities_api, name='friend_activities_api'),
]
