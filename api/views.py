from django.shortcuts import render

# Create your views here.

import json
from .models import Serie, DataPoint

from django.http import HttpResponse
from django.utils import timezone, dateparse

from django.contrib.auth import authenticate, login as blogin, logout as blogout
from django.contrib.auth.decorators import login_required

from django.db.models import F

def index(request):
  return HttpResponse("Hi worldies");

def login_challenge(request):
  return HttpResponse("{'code':'SUCCESS', 'csrf':'" + request.META.get("CSRF_COOKIE") + "'}")

def login(request):

  creds = json.loads(request.POST.get('creds'))
  
  user = authenticate(username=creds['username'],
                      password=creds['password'])
  
  if user is not None:
    blogin(request, user)
    return HttpResponse("{'code': ['LOGIN_SUCCESS']}")
  else:
    return HttpResponse("{'code': ['LOGIN_FAILED']}")

@login_required
def logout(request):
  blogout(request)
  return HttpResponse("{'code': ['LOGOUT_SUCCESS']}")
  
@login_required
def serie(request, serie_id=None):
  if request.method == "GET":
    return serie_get(request, serie_id)
  elif request.method == "POST":
    return serie_post(request, serie_id)
  elif request.method == "DELETE":
    return HttpResponse("{'code': ['NOT_IMPLEMENTED']}")

def serie_get(request, serie_id):

  try:
    serie = Serie.objects.get(id=serie_id)
  except:
    output = {}
    output['id'] = serie_id
    output['code'] = ['NOT_FOUND']
    return HttpResponse(json.dumps(output))

  output = {
    'id': serie_id,
    'code': ['SUCCESS'],
    'name': serie.name,
    'value_type': serie.value_type,
    'time_type': serie.time_type,
    'created': serie.created.isoformat(),
    'values': serie.values_as_list()
  }
    
  return HttpResponse(json.dumps(output))

def serie_post(request, serie_id):

  if serie_id is None:
    new_serie = Serie.objects.create(value_type = request.POST.get("value_type"),
                                     time_type = request.POST.get("time_type"),
                                     name = request.POST.get("name"))
    new_serie.save()
  else:
    try:
      serie = Serie.objects.get(id=serie_id)
    except:
      output['id'] = serie_id
      output['code'] = ['NOT_FOUND']
      return HttpResponse(json.dumps(output))
    if "value_type" in request.POST:
      serie.value_type = request.POST.get("value_type")
    if "time_type" in request.POST:
      serie.time_type = request.POST.get("time_type")
    if "name" in request.POST:
      serie.name = request.POST.get("name")
    serie.save()
    
  return HttpResponse(json.dumps({"code":["SUCCESS"]}))

@login_required
def datapoint(request, serie_id, datapoint_id=None):
  if request.method == "GET":
    return datapoint_get(request, serie_id, datapoint_id)
  elif request.method == "POST":
    return datapoint_post(request, serie_id, datapoint_id)
  elif request.method == "DELETE":
    return HttpResponse("{'code': ['NOT_IMPLEMENTED']}")

def datapoint_get(request, serie_id, datapoint_id):
  try:
    serie = Serie.objects.get(id=serie_id)
    datapoint = serie.datapoint_set.get(id=datapoint_id)
  except Serie.DoesNotExist:
    return HttpResponse("{'code': ['SERIE_NOT_FOUND']}")
  except DataPoint.DoesNotExist:
    return HttpResponse("{'code': ['DATAPOINT_NOT_FOUND']}")

  value = datapoint.get_value()
  time = datapoint.get_time()
      
  output = {
    'code': ['SUCCESS'],
    'value': value,
    'time': time
  }
  
  return HttpResponse(json.dumps(output))

def datapoint_post(request, serie_id, datapoint_id):

  if datapoint_id is None:
    try:
      datapoint = DataPoint()
      datapoint.value = request.POST['value']
      if 'time' in request.POST and request.POST['time'] != "":
        datapoint.time = dateparse.parse_datetime(request.POST['time'])
      else:
        datapoint.time = timezone.now()
      datapoint.serie = Serie.objects.get(id=serie_id)
      datapoint.save()
    except Serie.DoesNotExist:
      return HttpResponse("{'code': ['SERIE_NOT_FOUND']}")

  else:
    try:
      serie = Serie.objects.get(id=serie_id)
      datapoint = serie.datapoint_set.get(id=datapoint_id)
      if 'value' in request.POST and request.POST['time'] != "":
        datapoint.value = request.POST['value']
      if 'time' in request.POST and request.POST['value'] != "":
        datapoint.time = dateparse.parse_datetime(request.POST['time'])
      datapoint.save()
    except Serie.DoesNotExist:
      return HttpResponse("{'code': ['SERIE_NOT_FOUND']}")
    except DataPoint.DoesNotExist:
      return HttpResponse("{'code': ['DATAPOINT_NOT_FOUND']}")
    except:
      return HttpResponse("{'code': ['ERROR']}")

  return HttpResponse("{'code': ['SUCCESS']}")
