from django.http import HttpResponse
from django.template import loader
import utils

def index(request):
  #template = loader.get_template('movies/index.html')
  result = utils.getAllGenres()
  return HttpResponse(str(result))