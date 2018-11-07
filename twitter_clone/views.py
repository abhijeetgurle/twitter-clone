from django.http import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Tweet
from .models import Follow
from django.utils import timezone
from .forms import twitter

import django.shortcuts
from django.contrib.auth.models import User

# Create your views here.
def login_user(request):
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/feed')

	return render(request, 'twitter_clone/login.html', {})


def logout_user(request):
	logout(request)
	return HttpResponseRedirect('/')
	

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()
    return render(request, 'twitter_clone/signup.html', {'form': form})	


def feed(request):
    me= request.user
    tweets=[]
    f=list(Follow.objects.filter(follower=me))
    for i in range(f.__len__()):
        tweets.append(Tweet.objects.filter(author=f[i].following))
    return render(request, 'twitter_clone/feed.html', {'tweets':tweets})

def tweet(request):


    if request.method=='POST' :
        form = twitter(request.POST)
        if form.is_valid():
            #Tweet.text=request.POST['tweettext']
            Tweet.author=request.user
            Tweet.published_date=timezone.now()
            Tweet.save()
            return HttpResponseRedirect('/feed')
    else:
        form=twitter()
    return render(request,'/feed',{form:'form'})