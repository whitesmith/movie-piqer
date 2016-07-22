from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
import utils
import get
import json
from datetime import datetime as dt

def index(request):
  template = loader.get_template('movies/index.html')
  context = {}
  return HttpResponse(template.render(context, request))

def results(request):
  if request.method != "POST" or not request.POST.has_key('genre') or not request.POST.has_key('cast') or not request.POST.has_key('crew') or not request.POST.has_key('rating'):
    return redirect('/', permanent=True)

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
  if len(results) > 5:
    results = results[0:5]

  template = loader.get_template('movies/results.html')
  context = {
    'results' : results,
    'genres' : allGenres,
  }
  return HttpResponse(template.render(context, request))

def ifeellike(request):
  if request.method != "POST" or not request.POST.has_key('id'):
    return redirect('/', permanent=True)

  tmdbid = request.POST['id']
  result = utils.getMovieInfo(tmdbid)

  slug = get.tmdb2slug(tmdbid)
  poster = get.get_poster_image(slug)
  trailer = get.get_movie_trailer(slug).replace('watch?v=','embed/')
  images = result['images']['posters']
  if len(images)>4:
    images = images[0:4]

  template = loader.get_template('movies/ifeellike.html')
  context = {
    'result': result,
    'poster': poster,
    'trailer': trailer,
    'images': images,
    'slug': slug,
  }
  return HttpResponse(template.render(context, request))

def getcastcrewrating(request):
  if request.method != "POST" or not request.POST.has_key('slug'):
    return redirect('/', permanent=True)

  slug = request.POST['slug']
  cast = [get.get_people_image(x) for x in get.get_cast(slug)]
  cast = cast[0:6] if len(cast)>6 else cast
  crew = [get.get_people_image(x) for x in get.get_crew(slug)]
  crew = crew[0:6] if len(crew)>6 else crew
  rating = get.get_movie_rating(slug)
  data = {
    'cast': cast,
    'crew': crew,
    'rating': rating,
  }

  return HttpResponse(json.dumps(data))
