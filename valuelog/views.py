import json
import requests

from .models import Serie, DataPoint, LogUser

from django.core.exceptions import ValidationError

from django.http import HttpResponse
from django.utils import timezone, dateparse

from django.contrib.auth import authenticate, login as blogin, logout as blogout
from django.contrib.auth.decorators import login_required

from django.middleware.csrf import get_token

from django.db.models import F

from django.conf import settings

def index(request):
  return HttpResponse("Hi worldies");

def csrftoken(request):
  return request.META.get('CSRF_COOKIE') if request.META.get('CSRF_COOKIE') else get_token(request)

def register(request):
  try:
    recaptcha_result = requests.post(url='https://www.google.com/recaptcha/api/siteverify',
                                     data={
                                       'secret': settings.RECAPTCHA_SECRET_KEY,
                                       'response': request.POST.get('g-recaptcha-response'),
                                       # TODO: find out better way to get client IP reliably??
                                       'remoteip': request.META['HTTP_X_FORWARDED_FOR']
                                     }).json()

    if recaptcha_result['success']:
      newUser= LogUser.objects.validate_and_create_user(request.POST.get('username'),
                                                        request.POST.get('email'),
                                                        request.POST.get('password'))
      return HttpResponse(
        json.dumps({
          'code': ['REGISTER_SUCCESS'],
          'id': newUser.id
        })
      )
    else:
      raise Exception()
    
  except:
    return HttpResponse(json.dumps({'code': ['REGISTER_FAILED']}))

def login_challenge(request):
  return HttpResponse(json.dumps({'code':['SUCCESS'], 'csrf': csrftoken(request)}))

def login(request):

  if request.user.is_authenticated:
    return HttpResponse(json.dumps({'code': ['ALREADY_LOGGED_IN'], 'csrf': csrftoken(request)}))
  
  try:
    creds = json.loads(request.POST.get('creds'))
  except:
    creds = {'username': request.POST.get('username'),
             'password': request.POST.get('password')}
    
  user = authenticate(username=creds['username'],
                      password=creds['password'])
  
  if user is not None:
    blogin(request, user)
    return HttpResponse(json.dumps({'code': ['LOGIN_SUCCESS'], 'csrf':csrftoken(request)}))
  else:
    return HttpResponse(json.dumps({'code': ['LOGIN_FAILED'], 'csrf':csrftoken(request)}))

@login_required
def logout(request):
  blogout(request)
  return HttpResponse(json.dumps({'code': ['LOGOUT_SUCCESS'], 'csrf':csrftoken(request)}))

@login_required
def series(request):
  ss = Serie.objects.filter(owner=request.user.loguser.id)
  output = {
    'code':['SUCCESS'],
    'series': [serie.as_dict() for serie in ss]
  }
  return HttpResponse(json.dumps(output))

@login_required
def serie(request, serie_id=None):
  if request.method == "GET":
    return serie_get(request, serie_id)
  elif request.method == "POST":
    return serie_post(request, serie_id)
  elif request.method == "DELETE":
    return HttpResponse(json.dumps({"code": ["NOT_IMPLEMENTED"]}))

def serie_get(request, serie_id):

  try:
    serie = Serie.objects.get(id=serie_id)
  except:
    output = {}
    output['id'] = serie_id
    output['code'] = ["NOT_FOUND"]
    return HttpResponse(json.dumps(output))

  output = {
    'id': serie_id,
    'code': ["SUCCESS"],
    'name': serie.name,
    'value_type': serie.value_type,
    'time_type': serie.time_type,
    'created': serie.created.isoformat(),
    'values': serie.values_as_list()
  }
    
  return HttpResponse(json.dumps(output))

def serie_post(request, serie_id):

  if serie_id is None:
    try:
      new_serie = Serie(value_type = request.POST.get("value_type"),
                        time_type = request.POST.get("time_type"),
                        name = request.POST.get("name"),
                        owner = request.user.loguser)
      #validate the values
      new_serie.full_clean()

      #save if no exception was thrown
      new_serie.save()

      #for returning the id
      serie_id = new_serie.id
    except:
      output = {}
      output['code'] = ['NOT_CREATED','INVALID_DATA']
      return HttpResponse(json.dumps(output))

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
    
  return HttpResponse(json.dumps({"code":["SUCCESS"], 'id': serie_id}))

@login_required
def datapoint(request, serie_id, datapoint_id=None):
  if request.method == "GET":
    return datapoint_get(request, serie_id, datapoint_id)
  elif request.method == "POST":
    return datapoint_post(request, serie_id, datapoint_id)
  elif request.method == "DELETE":
    return HttpResponse(json.dumps({'code': ['NOT_IMPLEMENTED']}))

def datapoint_get(request, serie_id, datapoint_id):
  try:
    serie = Serie.objects.get(id=serie_id)
    datapoint = serie.datapoint_set.get(id=datapoint_id)
  except Serie.DoesNotExist:
    return HttpResponse(json.dumps({"code": ["SERIE_NOT_FOUND"]}))
  except DataPoint.DoesNotExist:
    return HttpResponse(json.dumps({"code": ["DATAPOINT_NOT_FOUND"]}))

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
        datapoint.time = request.POST['time']
      else:
        datapoint.time = timezone.now().isoformat()
      datapoint.serie = Serie.objects.get(id=serie_id)

      datapoint.validate_value()
      datapoint.validate_time()
      
      datapoint.full_clean()
      datapoint.save()
    except Serie.DoesNotExist:
      return HttpResponse(json.dumps({'code': ['SERIE_NOT_FOUND']}))
    except ValidationError as e:
      print(e)
      return HttpResponse(json.dumps({'code': ['INVALID_DATA']}))

  else:
    try:
      serie = Serie.objects.get(id=serie_id)
      datapoint = serie.datapoint_set.get(id=datapoint_id)
      if 'value' in request.POST and request.POST['time'] != "":
        datapoint.value = request.POST['value']
        datapoint.validate_value()
      if 'time' in request.POST and request.POST['value'] != "":
        datapoint.time = dateparse.parse_datetime(request.POST['time'])
        datapoint.validate_time()
      datapoint.full_clean()
      datapoint.save()
    except Serie.DoesNotExist:
      return HttpResponse(json.dumps({'code': ['SERIE_NOT_FOUND']}))
    except DataPoint.DoesNotExist:
      return HttpResponse(json.dumps({'code': ['DATAPOINT_NOT_FOUND']}))
    except ValidationError as e:
      print(e)
      return HttpResponse(json.dumps({'code': ['INVALID_DATA']}))
    except:
      return HttpResponse(json.dumps({'code': ['ERROR']}))

  return HttpResponse(json.dumps({'code': ['SUCCESS']}))
