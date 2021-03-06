from django.shortcuts import render

# Create your views here.

from api.models import Serie
from django.utils.safestring import mark_safe

import json

def index(request):
  series_list = Serie.objects.all()
  context = {
    'series_list': series_list
  }
  
  return render(request, 'ui/index.html', context)

def add_serie(request):
  return render(request, 'ui/add-serie.html', {})

def serie(request, serie_id):
  serie = Serie.objects.get(id=serie_id)
  datapoints = serie.datapoint_set.all()
  value_data = [ dp.get_value() for dp in datapoints ]
  time_data = [ dp.get_time() for dp in datapoints ]
  context = {
    'serie': serie,
    'datapoints': datapoints,
    'serie_json': mark_safe(json.dumps(serie.as_dict())),
    'values_json': mark_safe(json.dumps(value_data)),
    'times_json': mark_safe(json.dumps(time_data))
  }
  return render(request, 'ui/serie.html', context)
