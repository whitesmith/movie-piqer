from django.conf.urls import url

from . import views

app_name = 'movies'
urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^results$', views.results, name='results'),
  url(r'^ifeellike$', views.ifeellike, name='ifeellike'),
]