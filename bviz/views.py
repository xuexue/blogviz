# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
  ctx = {}
  return render(request, 'index.html', ctx)

def login_page(request):
  ctx = {}
  return render(request, 'login.html', ctx)

def logged_in(request):
  ctx = {}
  return render(request, 'logged_in.html', ctx)

def login_error(request):
  ctx = {}
  return render(request, 'login_error.html', ctx)

@login_required
def all_profiles(request):
  ctx = {}
  return render(request, 'profile.html', ctx)
