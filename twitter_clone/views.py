from django.shortcuts import render

# Create your views here.
def login(request):
	return render(request, 'twitter_clone/login.html', {})

def feed(request):
	return render(request, 'twitter_clone/feed.html', {})	