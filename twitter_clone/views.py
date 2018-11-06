from django.http import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login

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

def feed(request):
	return render(request, 'twitter_clone/feed.html', {})	