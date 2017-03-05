from django.conf.urls import url
from . import views

app_name = 'valuelog'

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^login$', views.login, name="login"),
    url(r'^login/challenge$', views.login_challenge, name="login_challenge"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^series$', views.series, name="series"),
    url(r'^serie$', views.serie, name="serie"),
    url(r'^serie/(?P<serie_id>[0-9]*)$', views.serie, name="serie"),
    url(r'^serie/(?P<serie_id>[0-9]*)/datapoint$', views.datapoint, name="datapoint"),
    url(r'^serie/(?P<serie_id>[0-9]*)/datapoint/(?P<datapoint_id>[0-9]*)$', views.datapoint, name="datapoint"),
]
