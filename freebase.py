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
	
def mql(dict,limit=1):
	if limit>1:
		cursor = True
	else:
		cursor = False
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
		return [entry.get("id",None) for entry in mql(query)]
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
	def actors(self):
		query={"id":self.id,"/film/film_character/portrayed_in_films":[{"actor":{"id":None},"film":{"initial_release_date":None},"sort":"film.initial_release_date"}]}
		res = [entry.get("actor",{"id":None})["id"] for entry in mql(query).get("/film/film_character/portrayed_in_films",[])]
		fin = []
		for i in res:
			try:
				fin.index(i)
			except ValueError:
				fin.append(i)
		return fin
	def movies(self):
		query={"id":self.id,"/film/film_character/portrayed_in_films":[{"film":{"id":None,"initial_release_date":None},"sort":"film.initial_release_date"}]}
		res = [entry.get("film",{"id":None})["id"] for entry in mql(query).get("/film/film_character/portrayed_in_films",[])]
		return res
	def nth_movie(self, n):
		movies - self.movies()
		if len(movies)>=(n-1):
			return movies[n-1]
		else:
			return None
	def actors_in_movie(self, movie):
		query = {"id":movie.id,"/film/film/starring":[{"character":{"id":self.id},"actor":{"id":None}}]}
		res = [entry.get("actor",{"id":None})["id"] for entry in mql(query).get("/film/film/starring",[])]
		return res
	def movies_for_actor(self,actor):
		query = {"id":self.id,"/film/film_character/portrayed_in_films":[{"film":{"id":None,"initial_release_date":None},"actor":{"id":actor.id},"sort":"film.initial_release_date"}]}
		res = [entry.get("film",{"id":None})["id"] for entry in mql(query).get("/film/film_character/portrayed_in_films",[])]
		return res
	def num_movies(self,actor):
		query = {"id":"/en/batman","/film/film_character/portrayed_in_films":{"return":"count"}}
		return mql(query).get("/film/film_character/portrayed_in_films",0)
	def num_movies_for_actor(self,actor):
		query = {"id":"/en/batman","/film/film_character/portrayed_in_films":{"actor":{"id":"/en/adam_west"},"return":"count"}}
		return mql(query).get("/film/film_character/portrayed_in_films",0)
	def nth_actor(self,n):
		actors = self.actors()
		if len(actors)>=(n-1):
			return actors[n-1]
		else:
			return None
	
def all_actors(limit=10):
	query = [{"type":"/film/actor","/common/topic/alias":[],"/film/actor/film":{"return":"count"},"name":None,"mid":None}]
	res = mql(query,limit)
	res.sort(key=(lambda val:-val.get("/film/actor/film",0)))
	out = []
	for r in res:
		id = r.get("mid","unknown")
		name = r.get("name")
		names = r.get("/common/topic/alias",[])
		if name != None:
			names.append(name)
		out.append((id,names))
	return out
	
def all_movies(limit=10):
	query = [{"type":"/film/film","/film/film/gross_revenue":None,"/common/topic/alias":[],"name":None,"mid":None,"/film/film/initial_release_date":None}]
	res = mql(query,limit)
	num_map = {'0':'9', '1':'8', '2':'7', '3':'6', '4':'5', '5':'4', '6':'3', '7':'2', '8':'1', '9':'0'}
	def invert_date(val):
		newstr = "";
		dat = val.get("/film/film/initial_release_date","9999-99-99");
		for charnum in range(len(dat)):
			newstr += num_map.get(dat[charnum],dat[charnum])
		return newstr
	res.sort(key=invert_date)
	out = []
	for r in res:
		id = r.get("mid","unknown")
		name = r.get("name")
		names = r.get("/common/topic/alias",[])
		if name != None:
			names.append(name)
		out.append((id,names))
	return out
	
def all_characters(limit=10):
	query = [{"type":"/film/film_character","name":None,"/common/topic/alias":[],"/film/film_character/portrayed_in_films":{"return":"count"}}]
	res = mql(query,limit)
	res.sort(key=(lambda val:val.get("/film/film_character/portrayed_in_films",0)))
	out = []
	for r in res:
		id = r.get("mid","unknown")
		name = r.get("name")
		names = r.get("/common/topic/alias",[])
		if name != None:
			names.append(name)
		out.append((id,names))
	return out
	