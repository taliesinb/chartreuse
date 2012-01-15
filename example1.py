#!/usr/bin/python

from chart import *
from rules import *
from freebase import *

t = trie()
t.add("who", ["word","who"])
t.add("directed", ["word","directed"])
t.add("Die Hard With A Vengeance", ["movie","/m/01_1hw"])
t.add("Die Hard", ["movie","/m/0p3_y"])

tokens = t.tokenize("who directed Die Hard?")
print "tokens", tokens
rules = [
  rule("start", ["query"]),
  rule("query", ["word", "word", "movie"], lambda w, d, m: movie(m.value).directors())
]

ch = chart(tokens, rules)

ch.print_rules()

winners = ch.parse(tokens)

print
print "winners:"
i = 0
for w in sorted(winners):
  print i, "\t", w
  i += 1