from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login_user'),
    path('logout_user', views.logout_user, name='logout_user'),
    path('feed', views.feed, name='feed'),
    path('signup',views.signup,name='signup'),
]
