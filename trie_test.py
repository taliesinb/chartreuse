from trie import *

t = trie() #"trie", 2)
t.clear()
t.add("who",["word",1])
t.add("directed",["word",2])
t.add("Die Hard",["movie",1])
t.add("Die Hard With a Vengeance",["movie",2])
t.save()
print "Result 1 = "+str(t.tokenize("who directed Die Hard?"))
print "Result 2 = "+str(t.tokenize("who directed Die Hard With a Vengeance?"))
#print t.db.root.keys()
t.save()
t.finish()