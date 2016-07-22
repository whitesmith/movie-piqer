from django.http import HttpResponse
from django.template import loader
import utils
import json
from datetime import datetime as dt

def index(request):
  template = loader.get_template('movies/index.html')
  context = {}
  return HttpResponse(template.render(context, request))

def results(request):
  if request.method != "POST" or not request.POST.has_key('genre') or not request.POST.has_key('cast') or not request.POST.has_key('crew') or not request.POST.has_key('rating'):
    return index(request)

  allGenres = utils.getAllGenres()['genres']
  genres=[]
  for x in request.POST['genre'].split("|"):
    for y in allGenres:
      if x.lower() == y['name'].lower():
        genres.append(y['id'])
  cast = []
  for x in request.POST['cast'].split(","):
    if len(x)!=0:
      tmp = utils.findPerson(x)
      if tmp.has_key('results') and len(tmp['results'])!=0:
        cast.append(tmp['results'][0]['id'])
  crew = []
  for x in request.POST['crew'].split(","):
    if len(x)!=0:
      tmp = utils.findPerson(x)
      if tmp.has_key('results') and len(tmp['results'])!=0:
        crew.append(tmp['results'][0]['id'])
  rating = request.POST['rating']

  tmp = utils.discoverMovie(genres,rating,cast,crew)['results']
  results = []
  for x in tmp:
    if dt.strptime(x['release_date'],"%Y-%m-%d") <= dt.now():
      results.append(x)

  template = loader.get_template('movies/results.html')
  context = {
    'results' : results,
  }
  return HttpResponse(template.render(context, request))