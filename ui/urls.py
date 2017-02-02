from django.conf.urls import url
from . import views

app_name = 'ui'
urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^serie/(?P<serie_id>[0-9]*)/$', views.serie, name="serie"),
  url(r'^add-serie/$', views.add_serie, name="add_serie"),
]
