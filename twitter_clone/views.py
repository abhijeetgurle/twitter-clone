from django.http import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm
from .models import Tweet
from .models import Follow
from .models import HashTag
from django.utils import timezone
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
    if request.method=='POST' :

        #Tweet.text=request.POST['tweettext']
        #Tweet.author=request.user
        #Tweet.published_date=timezone.now()
        Tweet.objects.create(text=request.POST.get('tweettext'),author=request.user,likes=0)
        #Tweet.save()
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


def follower(request):
	logged_in_user = request.user
	following_user_object = Follow.objects.filter(following=logged_in_user)
	following_user_username = []
	for i in range(following_user_object.__len__()):
		following_user_username.append(User.objects.get(username=(following_user_object[i].follower).username))
	return render(request,'twitter_clone/follower.html',{'query':following_user_username})


def my_activities(request):
	logged_in_user = request.user
	my_tweets = Tweet.objects.filter(author=logged_in_user)
	return render(request,'twitter_clone/my_activities.html',{'my_tweets' :my_tweets})

def profile(request):
    logged_in_user = request.user
    tweet_cnt=Tweet.objects.filter(author=logged_in_user).count
    likes=0
    tweet=Tweet.objects.filter(author=logged_in_user)
    for t in tweet:
        likes +=t.likes
    follower=Follow.objects.filter(follower=logged_in_user).count()
    following=Follow.objects.filter(following=logged_in_user).count()
    user1=User.objects.filter(username=logged_in_user)

    if request.method=='POST':
        User.objects.filter(username=logged_in_user).update(first_name=request.POST.get('first_name'),
                                                            last_name=request.POST.get('last_name'),
                                                            username=request.POST.get('username'),
                                                            email=request.POST.get('email'),
                                                           )
        u=user1[0]
        u.set_password(request.POST.get('password'))
        u.save()

    context={
        'tweet_cnt':tweet_cnt,
        'follower':follower,
        'following':following,
        'user1':user1[0],
        'likes':likes
    }
    return render(request,'twitter_clone/profile.html',context)


def hashtags(request):
    hashtag_list = HashTag.objects.all()
    return render(request,'twitter_clone/hashtags.html',{'hashtag_list' :hashtag_list})    