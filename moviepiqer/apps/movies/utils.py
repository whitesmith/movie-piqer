from urllib2 import Request, urlopen
from urllib import urlencode
import os

base_url="http://api.themoviedb.org/3/"

base_headers = {
  'Content-Type': 'application/json',
}

base_data = {
  'api_key': os.environ.get('TMDB_API_KEY','')
}

def makeRequest(url, data=base_data, headers=base_headers):
  params = urlencode(data)
  request = Request(url+params, headers=headers)
  print url+"/?"+params
  return urlopen(request).read()

def getAllGenres():
  url = base_url+"genre/movie/list"
  return makeRequest(url)