from django.conf.urls import url
from . import views

app_name = 'api'

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^serie/$', views.serie, name="serie"),
  url(r'^serie/(?P<serie_id>[0-9]*)/$', views.serie, name="serie"),
  url(r'^serie/(?P<serie_id>[0-9]*)/datapoint/$', views.datapoint, name="datapoint"),
  url(r'^serie/(?P<serie_id>[0-9]*)/datapoint/(?P<datapoint_id>[0-9]*)$', views.datapoint, name="datapoint"),
]
