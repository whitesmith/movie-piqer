from urllib.request import Request, urlopen
import re
import matplotlib.pyplot as plt

headers = {
  'Content-Type': 'application/json',
  'trakt-api-version': '2',
  'trakt-api-key': 'b1ef6c74877916f3adf45032946bedc850d325827fb3e81306e91225aafa86e2'
}

def get_related(slug):
	
	request = Request('https://api.trakt.tv/movies/'+slug+'/related', headers=headers)
	response_body = str(urlopen(request).read())

	related = re.findall(r"""("title":"(?P<title>[^"]*)")[^}]*slug":"(?P<sl>[^"]*)"[^}]*imdb":"(?P<id>[^"]*)\"""", response_body)

	all_movies, all_counts, all_slugs = [], [], []

	for movies in related:
		movie_title = list(movies)[1]
		movie_slug = list(movies)[2]
		movie_id = list(movies)[3]
		
		if str(movie_title) in all_movies:
			idx = all_movies.index(str(movie_title))
			all_counts[idx] = all_counts[idx]+1
		else:
			all_movies.append(str(movie_title))
			all_slugs.append(str(movie_slug))
			all_counts.append(1)

		request = Request('https://api.trakt.tv/movies/'+movie_slug+'/related', headers=headers)
		response_body = str(urlopen(request).read())
		got1 = re.findall(r"""("title":"(?P<title>[^"]*)")[^}]*slug":"(?P<sl>[^"]*)"[^}]*imdb":"(?P<id>[^"]*)\"""", response_body)
		for movies1 in got1:
			#print('\t'+str(list(movies1)[1]))
			movie_title1 = str(list(movies1)[1])
			movie_slug1 = list(movies1)[2]
			movie_id1 = list(movies1)[3]

			if movie_title1 not in all_movies:
				all_movies.append(movie_title1)
				all_slugs.append(str(movie_slug1))
				all_counts.append(1)
			else:
				idx = all_movies.index(movie_title1)
				all_counts[idx] = all_counts[idx]+1

	
	# Add cast scoring
	cast = get_cast(slug)

	for people_slug in cast:
		movie_titles, movie_slugs, movie_imdbs = get_movie_person(people_slug)
		#print(got2)
		for movie in movie_titles:
			if movie in all_movies:
				idx = all_movies.index(movie)
				all_counts[idx] = all_counts[idx]+1

	# Add genre scoring
	for m in range(len(all_slugs)):
		movie_slug = all_slugs[m]
		genre_comp = get_genres(movie_slug)
		genres = get_genres(slug)
		g = 0
		for gr in genre_comp:
			if gr in genres:
				g = g + 1
		all_counts[m] = all_counts[m] + g
	
	all_counts, all_movies, all_slugs = zip(*sorted(zip(all_counts, all_movies, all_slugs)))
	all_counts, all_movies, all_slugs = list(all_counts[::-1]), list(all_movies[::-1]), list(all_slugs[::-1])

	# Add name scoring


	# Remove queried movie from lists
	idx = all_slugs.index(slug)
	del all_counts[idx]
	del all_movies[idx]
	del all_slugs[idx]

	#for i in range(len(all_movies)):
	#	print('['+str(all_counts[i])+']: '+str(all_movies[i]))

	return all_counts, all_slugs, all_movies

def get_movie_person(slug):
	request = Request('https://api.trakt.tv/people/'+slug+'/movies', headers=headers)
	response_body = str(urlopen(request).read())
	got = re.findall(r"""("title":"(?P<title>[^"]*)")[^}]*slug":"(?P<sl>[^"]*)"[^}]*imdb":"(?P<id>[^"]*)\"""", response_body)
	movie_titles = []
	movie_slugs  = []
	movie_imdbs  = []
	for items in got:
		movie_titles.append(str(list(items)[1]))
		movie_slugs.append(str(list(items)[2]))
		movie_imdbs.append(str(list(items)[3]))
	return movie_titles, movie_slugs, movie_imdbs

def get_crew(slug):

	request = Request('https://api.trakt.tv/movies/'+slug+'/people', headers=headers)
	response_body = str(urlopen(request).read())
	crew_p = re.findall(r"""crew[^}]*("slug":"(?P<slug>[^"]*)")[^}]*("imdb":"(?P<id>[^"]*)")[^}]*""", response_body)

	crew = []
	for people in crew_p:
		crew.append(str(list(people)[1]))
	return crew
	

	
	#print(response_body)

def get_cast(slug):

	request = Request('https://api.trakt.tv/movies/'+slug+'/people', headers=headers)
	response_body = str(urlopen(request).read())
	cast_p = re.findall(r"""character[^}]*("slug":"(?P<slug>[^"]*)")[^}]*("imdb":"(?P<id>[^"]*)")[^}]*""", response_body)

	cast = []
	for people in cast_p:
		cast.append(str(list(people)[1]))
	return cast
	

	
	#print(response_body)

def slug2tmdb(slug, type):
	if type=='movie':
		request = Request('https://api.trakt.tv/movies/'+slug, headers=headers)
	else:
		request = Request('https://api.trakt.tv/people/'+slug, headers=headers)
	response_body = str(urlopen(request).read())
	#print(response_body)
	tmdb_p = re.findall(r"""("tmdb":(?P<tmdb>[^"}]*))""", response_body)
	#print(tmdb_p)
	tmdb   = str(list(tmdb_p[0])[1])

	return tmdb

def slug2imdb(slug, type):
	if type=='movie':
		request = Request('https://api.trakt.tv/movies/'+slug, headers=headers)
	else:
		request = Request('https://api.trakt.tv/people/'+slug, headers=headers)
	response_body = str(urlopen(request).read())
	#print(response_body)
	imdb_p = re.findall(r"""("imdb":"(?P<imdb>[^"}]*)")""", response_body)
	#print(imdb_p)
	imdb   = str(list(imdb_p[0])[1])

	return imdb

def tmdb2slug(tmdb):
	request = Request('https://api.trakt.tv/search/tmdb/'+tmdb, headers=headers)
	response_body = str(urlopen(request).read())

	slug_p = re.findall(r"""("slug":"(?P<slug>[^"]*)")""", response_body)
	slug   = str(list(slug_p[0])[1])

	return slug

def imdb2slug(imdb):
	request = Request('https://api.trakt.tv/search/imdb/'+imdb, headers=headers)
	response_body = str(urlopen(request).read())

	slug_p = re.findall(r"""("slug":"(?P<slug>[^"]*)")""", response_body)
	slug   = str(list(slug_p[0])[1])

	return slug

def get_genres(slug):
	print('https://api.trakt.tv/movies/'+slug+'?extended=full')
	request = Request('https://api.trakt.tv/movies/'+slug+'?extended=full', headers=headers)
	#print(urlopen(request).url)
	response_body = str(urlopen(request).read())

	genres_p = re.findall(r"""\"genres\":\[([^\]]*)\]""", response_body)
	genres_p = str(list(genres_p)[0])
	genres = genres_p.replace("\"", "").split(',')

	#genres = []
	#for genre in genres_p:
	#	genres.append(str(list(genre)[1]))

	return genres

def get_poster_image(slug):

	request = Request('https://api.trakt.tv/movies/'+slug+'?extended=images', headers=headers)
	response_body = str(urlopen(request).read())
	poster_p = re.findall(r"""("poster":{"full":"(?P<poster>[^"]*)")""", response_body)
	poster   = str(list(poster_p[0])[1])
	return poster

def get_people_image(slug):

	request = Request('https://api.trakt.tv/people/'+slug+'?extended=images', headers=headers)
	response_body = str(urlopen(request).read())
	#print(response_body)
	image_p = re.findall(r"""("headshot":{"full":"(?P<image>[^"]*)")""", response_body)
	image   = str(list(image_p[0])[1])
	return image

def get_movie_trailer(slug):

	request = Request('https://api.trakt.tv/movies/'+slug+'?extended=full', headers=headers)
	response_body = str(urlopen(request).read())
	#print(response_body)
	trailer_p = re.findall(r"""("trailer":"(?P<trailer>[^"]*)")""", response_body)
	trailer   = str(list(trailer_p[0])[1])
	return trailer

def get_movie_rating(slug):

	# Trakt
	request = Request('https://api.trakt.tv/movies/'+slug+'/ratings', headers=headers)
	response_body = str(urlopen(request).read())
	#print(response_body)
	trakt_p = re.findall(r"""("rating":(?P<trakt>[^"]*),)""", response_body)
	#print(trakt_p)
	trakt   = str(list(trakt_p[0])[1])

	# Metacritic
	imdb_id = slug2imdb(slug, 'movie')
	#print(imdb_id)
	request = Request('http://www.omdbapi.com/?i='+imdb_id+'&r=json&tomatoes=true', headers=headers)
	response_body = str(urlopen(request).read())
	print(response_body)
	meta_p = re.findall(r"""("Metascore":\"(?P<meta>[^"]*)\")""", response_body)
	meta   = str(list(meta_p[0])[1])


	# IMDB
	imdb_p = re.findall(r"""("imdbRating":\"(?P<imdb>[^"]*)\")""", response_body)
	#print(trakt_p)
	imdb   = str(list(imdb_p[0])[1])

	# Rotten Tomatoes
	tomatu_p = re.findall(r"""("tomatoUserMeter":\"(?P<tomat>[^"]*)\")""", response_body)
	tomatu   = str(list(tomatu_p[0])[1])

	tomatc_p = re.findall(r"""("tomatoMeter":\"(?P<tomat>[^"]*)\")""", response_body)
	tomatc   = str(list(tomatc_p[0])[1])



	return trakt, meta, imdb, tomatu, tomatc

def get_genre_list():

	request = Request('https://api.trakt.tv/genres/movies', headers=headers)
	response_body = str(urlopen(request).read())
	genres_p = re.findall(r"""("name":\"(?P<genre>[^"]*)\")""", response_body)
	
	genres_list = []
	for genre in genres_p:
		genres_list.append(str(list(genre)[1]))

	return genres_list

def get_random_slug():
	request = Request('http://www.imdb.com/random/title', headers=headers)
	url = urlopen(request).url
	imdb_p = re.findall(r"""(/title/(?P<genre>[^\/]*)\/)""", url)
	#print(imdb_p)
	imdb = str(list(imdb_p[0])[1])

	slug = imdb2slug(imdb)

	return slug


def get_genre_ratings_stats(slug_list):

	r1, r2, r3 = [], [], []
	i=0
	
	for slug in slug_list:
		r = list(get_movie_rating(slug))
		r1.append(r[0])
		r2.append(r[1])
		r3.append(r[2])

	return r1, r2, r3

def get_in_theatres():
	request = Request('https://api.trakt.tv/movies/boxoffice', headers=headers)
	response_body = str(urlopen(request).read())
	movies = re.findall(r"""("slug":"(?P<slug>[^"]*)")""", response_body)

	movie_slugs =[]
	for movie in movies:
		movie_slugs.append(str(list(movie)[1]))

	return movie_slugs
		
def get_popular():
	request = Request('https://api.trakt.tv/movies/popular', headers=headers)
	response_body = str(urlopen(request).read())
	movies = re.findall(r"""("slug":"(?P<slug>[^"]*)")""", response_body)

	movie_slugs =[]
	for movie in movies:
		movie_slugs.append(str(list(movie)[1]))

	return movie_slugs


print(get_movie_rating('terminator-genisys-2015'))

#print(get_in_theatres())
#print(get_popular())

#r1, r2, r3 = get_genre_ratings_stats('action')
#print(len(r1),len(r2),len(r3))
# n, bins, patches = plt.hist(r1, 50, normed=1, facecolor='green', alpha=0.75)
# plt.show()
# n, bins, patches = plt.hist(r2, 50, normed=1, facecolor='green', alpha=0.75)
# plt.show()
# n, bins, patches = plt.hist(r3, 50, normed=1, facecolor='green', alpha=0.75)
# plt.show()

#print(get_random_slug())

#print(get_genre_list())

# ---- Filmes relacionados ---- 
# all_counts, all_slugs, all_movies = get_related('terminator-genisys-2015')

# for i in range(len(all_movies)):
# 	print('['+str(all_counts[i])+']: '+str(all_movies[i])+' ('+str(all_slugs[i])+')')

# ---- Movie rating
# print(get_movie_rating('insurgent-2015'))

# ---- Cast de um filme ---- 
# cs = get_cast('insurgent-2015')
# print()
# for people in cs:
#  	print(slug2imdb(people, 'people'))

# ---- Movie genre ---- 
# genres = get_genres('insurgent-2015')
# print(genres)

# ---- Movie poster/Person headshot ---- 
#print(get_poster_image('insurgent-2015'))
#print(get_people_image('shailene-woodley'))

# ---- Conversões de ids ---- 
#print(tmdb2slug('94185'))
#print(imdb2slug('nm0940362'))
#print(slug2tmdb('insurgent-2015', 'movie'))


# ---- ---- ---- Outras sem parsing ----  ----  ---- 

# ---- Search by query and genre ---- 
#request = Request('https://api.trakt.tv/search/movie?query=insurgent&extended=full&genres=action', headers=headers)

# ---- List genres ---- 
#request = Request('https://api.trakt.tv/genres/movies', headers=headers)

# ---- Search by rating ---- 
#request = Request('https://api.trakt.tv/search/movie?query=insurgent&extended=full&ratings=75-100', headers=headers)

# ---- Get movie com id do imdb ---- 
#request = Request('https://api.trakt.tv/search/imdb/tt0848228', headers=headers)

# ---- Get movie com id do trakt ---- 
#request = Request('https://api.trakt.tv/search/trakt/161414', headers=headers)

# ---- Get movie com slug do trakt ---- 
#request = Request('https://api.trakt.tv/movies/insurgent-2015', headers=headers)

# ---- Movie related com filtros ---- 
#request = Request('https://api.trakt.tv/movies/insurgent-2015/related', headers=headers)

# ---- Informacao completa do filme sem cast ---- 
#request = Request('https://api.trakt.tv/movies/insurgent-2015?extended=full,images', headers=headers)

# ---- Informacao completa de um ator ---- 
#request = Request('https://api.trakt.tv//people/shailene-woodley?extended=full', headers=headers)

# ---- Filmes de um ator / Search por cast ou crew ---- 
#request = Request('https://api.trakt.tv/people/shailene-woodley/movies', headers=headers)

# ----  Box office, Popular ---- 
#request = Request('https://api.trakt.tv/movies/boxoffice', headers=headers)
#request = Request('https://api.trakt.tv/movies/popular', headers=headers)







