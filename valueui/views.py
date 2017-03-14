from django.shortcuts import render

# Create your views here.

from valuelog.models import Serie
from django.utils.safestring import mark_safe

import json

def index(request):
  context = {
    "pagename": "main",
    "loggedIn": request.user.is_authenticated
  }
  return render(request, 'ui/main-page.html', context)

def login(request):
  context = {
    "pagename": "login",
    "loggedIn": request.user.is_authenticated
  }
  return render(request, 'ui/login-page.html', context)

def register(request):
  context = {
    "pagename": "register",
    "loggedIn": request.user.is_authenticated
  }
  return render(request, 'ui/register-page.html', context)

def about(request):  
  context = {
    "pagename": "about",
    "loggedIn": request.user.is_authenticated
  }
  return render(request, 'ui/about-page.html', context)

def series(request):
  context = {
    "pagename": "series",
    "loggedIn": request.user.is_authenticated,
    "value_type_options": Serie.VALUE_TYPE,
    "time_type_options": Serie.TIME_TYPE
  }
  return render(request, 'ui/series-page.html', context)

def add_serie(request):
  return render(request, 'ui/add-serie.html', {})

def serie(request, serie_id):
  context = {
    "pagename": "serie-" + str(serie_id),
    "loggedIn": request.user.is_authenticated,
    "serie_id": serie_id
  }
  return render(request, 'ui/serie-page.html', context)
