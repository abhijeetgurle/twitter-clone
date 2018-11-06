from django.http import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm

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
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'twitter_clone/signup.html', {'form': form})	


def feed(request):
	return render(request, 'twitter_clone/feed.html', {})	