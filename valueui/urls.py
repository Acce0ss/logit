from django.conf.urls import url
from . import views

app_name = 'valueui'

urlpatterns = [
  url(r'^$', views.index, name="index"),
  url(r'^login$', views.login, name="login"),
  url(r'^register$', views.register, name="register"),
  url(r'^about$', views.about, name="about"),
  url(r'^series$', views.series, name="series"),
  url(r'^serie/(?P<serie_id>[0-9]*)/$', views.serie, name="serie"),
  url(r'^add-serie/$', views.add_serie, name="add_serie"),
]
