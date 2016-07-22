from urllib2 import Request, urlopen
from urllib import urlencode
import os
import json

base_url="http://api.themoviedb.org/3/"

base_headers = {
  'Content-Type': 'application/json',
}

base_data = {
  'api_key': os.environ.get('TMDB_API_KEY','')
}

def makeRequest(url, data=base_data, headers=base_headers):
  params = urlencode(data)
  request = Request(url+"?"+params, headers=headers)
  print url+"?"+params
  return urlopen(request).read()

def getAllGenres():
  url = base_url+"genre/movie/list"
  return json.loads(makeRequest(url))

def findPerson(name):
  url = base_url+"search/person"
  data = base_data.copy()
  data['query'] = name
  return json.loads(makeRequest(url, data=data))

def discoverMovie(genres=[],rating=0.0,cast=[],crew=[]):
  url = base_url+"discover/movie"
  data = base_data.copy()
  if len(genres) != 0:
    data['with_genres'] = ""
    for genre in genres:
      data['with_genres'] = data['with_genres']+str(genre)+"|"
  if rating >  0.0 and rating <= 10.0:
    data['vote_average.gte'] = str(rating)
  if len(cast) != 0:
    data['with_cast'] = ""
    for person in cast:
      data['with_cast'] = data['with_cast']+str(person)+","
  if len(crew) != 0:
    data['with_crew'] = ""
    for person in crew:
      data['with_crew'] = data['with_crew']+str(person)+","
  data['sort_by'] = 'popularity.desc'
  return json.loads(makeRequest(url, data=data))