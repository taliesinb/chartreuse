from trie import *

t = trie();

t.add("rob",("guy",1))
t.add("robert",("guy",2),True)
t.add("lockhart",("guy",3))
t.diff()
t.tokenize("robert lockhart")
t.tokenize("robert glorb lockhart")