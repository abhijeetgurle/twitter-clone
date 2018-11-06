from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('feed/', views.feed, name='feed'),
    path('signup',views.signup,name='signup'),
]
