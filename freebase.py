import urllib, json

def rawget(url):
	page = urllib.urlopen(url)
	results = page.read()
	page.close()
	return results

def mql_string(query,cursor=None):
	url = "https://api.freebase.com/api/service/mqlread?query={\"query\":"
	url = url+query
	if cursor!=None:
		url = url+",\"cursor\":"+cursor
	url = url+"}"
	return rawget(url)
	
def mql(dict,cursor=True,limit=2):
	if not cursor:
		res = json.loads(mql_string(json.dumps(dict))).get("result",None)
		if res==None:
			raise Exception("no result from freebase")
		else:
			return res
	else:
		ret = json.loads(mql_string(json.dumps(dict),"true"))
		cursor = ret.get("cursor")
		res = ret.get("result",[])
		while cursor!=False and limit>0:
			limit = limit - 1
			ret = json.loads(mql_string(json.dumps(dict),cursor))
			cursor = ret.get("cursor")
			res1 = ret.get("result",[])
			for i in res1:
				res.append(i)
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
	
def all_actors():#This needs to be broken down by letter with "name~=":"A*"..."B*"...etc.
	query = [{"type":"/film/actor","/common/topic/alias":[],"/film/actor/film":{"return":"count"},"name":None,"mid":None,"limit":10000}]
	res = mql(query,True,10)
	res.sort(key=(lambda val:-val.get("/film/actor/film",0)))
	out = dict([])
	for r in res:
		id = r.get("mid","unknown")
		name = r.get("name")
		names = r.get("/common/topic/alias",[])
		if name != None:
			names.append(name)
		out[id] = names
	return out
	
def all_movies():
	query = [{"type":"/film/film","/film/film/gross_revenue":None,"/common/topic/alias":[],"name":None,"mid":None,"sort":"/film/film/gross_revenue"}]