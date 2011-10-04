from trie import *

t = trie("trie",2)
t.clear()
t.add("rob",["guy",1])
t.add("robert",["guy",2])
t.add("lockhart",["guy",3])
t.save()
print t.tokenize("robert lockhart")
print t.tokenize("robert glorb lockhart")
print t.db.root.keys()
t.save()
t.finish()