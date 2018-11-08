from django.http import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Tweet
from .models import Follow
from django.utils import timezone
from .forms import twitter
from .forms import UserFollower
from django.db.models import Q

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


def following(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		method = request.POST.get('method')
		user = User.objects.get(username=username)

		if(method=='unfollow'):
			Follow.objects.filter(Q(follower=request.user) & Q(following=user)).delete()
			return HttpResponseRedirect('/following')

		else:
			Follow.objects.create(follower=request.user, following=user)
			print("entry added successfully")
			return HttpResponseRedirect('/following')			

	logged_in_user = request.user
	followed_user_object = Follow.objects.filter(follower=logged_in_user)

	followed_user_username = []
	for i in range(followed_user_object.__len__()):
		followed_user_username.append(User.objects.get(username = (followed_user_object[i].following).username))	
			
	users_excluded = []
	for i in range(followed_user_username.__len__()):		
		users_excluded.append(followed_user_username[i]) 
	users_excluded.append(User.objects.get(username = logged_in_user))
	
	all_users = list(User.objects.all())
	not_followed_user = [x for x in all_users if x not in users_excluded]

	return render(request, 'twitter_clone/following.html', {'followed_user_objects':followed_user_username, 'not_followed_user_objects' :not_followed_user})


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