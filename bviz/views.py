# Create your views here.
from django.shortcuts import render

def index(request):
  ctx = {}
  return render(request, 'index.html', ctx)

def logged_in(request):
  ctx = {}
  return render(request, 'logged_in.html', ctx)

def login_error(request):
  ctx = {}
  return render(request, 'logged_in.html', ctx)

def all_profiles(request):
  return render(request, '', ctx)
