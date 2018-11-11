from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('signup',views.signup,name='signup'),
    path('feed', views.feed, name='feed'),
    path('following', views.following, name='following'),
    path('follower',views.follower,name='follower'),
    path('my_activities',views.my_activities, name='my_activities'),
    path('profile',views.profile,name='profile'),
    path('hashtags',views.hashtags,name='hashtags'),
]
