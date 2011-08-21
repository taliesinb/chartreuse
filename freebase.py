import urllib, json

def rawget(url):
	page = urllib.urlopen(url)
	results = page.read()
	page.close()
	return results

def mql_string(query):
	url = "https://api.freebase.com/api/service/mqlread?query={\"query\":"
	url = url+query+"}"
	return rawget(url)
	
def mql(dict):
	res = json.loads(mql_string(json.dumps(dict))).get("result",None)
	if res==None:
		raise Exception("no result from freebase")
	else:
		return res
	
class movie:
	def __init__(self, id):
		self.id = id
	def directors(self):
		res = mql({"id":self.id,"/film/film/directed_by":[{"id":None}]})
		res = res.get("/film/film/directed_by",[])
		return [entry.get("id",None) for entry in res]
	def writers(self):
		res = mql({"id":self.id,"/film/film/written_by":[{"id":None}]})
		res = res.get("/film/film/written_by",[])
		return [entry.get("id",None) for entry in res]
	def actors(self):
		res = mql({"id":self.id,"/film/film/starring":[{"character":{"id":None},"actor":{"id":None}}]})
		res = res.get("/film/film/starring",[])
		return [{"character":role.get("character",{"id":None}).get("id"), "actor":role.get("actor",{"id":None}).get("id")} for role in res]
	def actors_in_common(self, movie):
		query = [{"type":"/film/actor","id":None,"/film/actor/film":{"/film/performance/film":{"id":(self.id)}},"ns0:/film/actor/film":{"/film/performance/film":{"id":(movie.id)}}}]
		res = mql(query)
		return [entry.get("id",None) for entry in res]
	def characters_in_common(self,movie):
		query = [{"type":"/film/film_character","id":None,"/film/film_character/portrayed_in_films":{"/film/performance/film":{"id":self.id}},"ns0:/film/film_character/portrayed_in_films":{"/film/performance/film":{"id":movie.id}}}]
		return [entry.get("id",None) for entry in mql(query)]
	def release_date(self):
		query = {"id":self.id,"/film/film/initial_release_date":{"value":None}}
		res = mql(query)
		return res.get("/film/film/initial_release_date",{"value":None}).get("value")
	def genres(self):
		return mql({"id":self.id,"/film/film/genre":[]}).get("/film/film/genre",[])
		
#DIRECTORS AND WRITERS GO HERE

class actor:
	def __init__(self, id):
		self.id = id
	def movies(self):
		query = {"id":self.id, "/film/actor/film" : [{"/film/performance/film":{"id":None}, "/film/performance/character":{"id":None}}]}
		return [{"film":show.get("/film/performance/film",{"id":None}).get("id"),"character":show.get("/film/performance/character",{"id":None}).get("id")} for show in mql(query).get("/film/actor/film",[])]
	def movies_in_common(self, actor):
		query = [{"type":"/film/film","id":None,"/film/film/starring":[{"actor":{"id":self.id}}],"ns0:/film/film/starring":[{"actor":{"id":actor.id}}]}]
		return [entry.get("id",None) for entry in mql(query)]
	def characters_in_common(self, actor):
		query = [{"type": "/film/film_character","id":None,"/film/film_character/portrayed_in_films": [{"actor": {"id":self.id}}],"ns0:/film/film_character/portrayed_in_films": [{"actor": {"id":actor.id}}]}]
	def nth_movie(self,n):
		query = [{"type":"/film/film","id":None,"/film/film/starring":{"actor":{"id":self.id}},"initial_release_date":None,"sort": "initial_release_date","limit":n}]
		res = mql(query)
		if len(res)<n:
			return None
		else:
			return res[n-1].get("id",None)
	def num_movies(self):
		query = [{"id":self.id,"/film/actor/film":{"return":"count"}}]
		return mql(query).get("/film/actor/film",None)
		
class character:
	def __init__(self, id):
		self.id = id
	#TODO: actors, movies, actors in movie, movies for actor
	#TODO: nth actor to portray