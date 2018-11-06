from django.shortcuts import render

# Create your views here.
def login(request):
	return render(request, 'twitter_clone/login.html', {})

def feed(request):
	return render(request, 'twitter_clone/feed.html', {})

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm

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