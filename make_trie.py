#trie - constructor script
# this should eventually become a cron job

import trie, freebase

TRUNK_WORDS = 1000
TRUNK_ACTORS = 1000
TRUNK_MOVIES = 1000
TRUNK_CHARACTERS = 1000

def make_trie(test=False):
	############ WORDS #############
	t = trie.trie()
	wordlist = open("wordlist.txt","r")
	num_words = 0
	parts = wordlist.readline()
	while parts != "":
		parts = parts.split()
		if len(parts)>3 and int(parts[3])>1:
			num_words+=1
			t.add(parts[1],("word",parts[1]),num_words<=TRUNK_WORDS)
		parts = wordlist.readline()
	wordlist.close()
	############ ACTORS ############
	actorlist = freebase.all_actors(1 if test else 1000)
	for i in range(len(actorlist)):
		for j in actorlist[i][1]:
			t.add(j,("actor",actorlist[i][0]), i<TRUNK_ACTORS)
	############ MOVIES ############
	movielist = freebase.all_movies(1 if test else 1000)
	for i in range(len(movielist)):
		for j in movielist[i][1]:
			t.add(j,("movies",actorlist[i][0]), i<TRUNK_MOVIES)
	############ CHARACTERS ########
	characterlist = freebase.all_characters(1 if test else 1000)
	for i in range(len(characterlist)):
		for j in characterlist[i][1]:
			t.add(j,("char",characterlist[i][0]),i<TRUNK_CHARACTERS)
	t.diff()

make_trie(True)