#!/usr/bin/python

from chart import *
from rules import *

"""tokens = [
  symbol("buffalo", "Buffalo-born", (0,1)),
  symbol("buffalo", "Bison",        (1,2)),  
  symbol("buffalo", "Buffalo-born", (2,3)),
  symbol("buffalo", "Bison",        (3,4)),
  symbol("buffalo", "bully",        (4,5)),
  symbol("buffalo", "bully",        (5,6)),
  symbol("buffalo", "Buffalo-born", (6,7)),
  symbol("buffalo", "Bison",        (7,8))
]"""

t = trie()
t.add("buffalo", ("buffalo","Buffalo-born"))
t.add("buffalo", ("buffalo","Bison"))
t.add("buffalo", ("buffalo","bully"))
t.add(" ",("space",1))

tokens = t.tokenize("buffalo buffalo buffalo")
print "tokens", tokens
rules = [
  rule("start", ["sentence"]),
  rule("sentence", ["noun_phrase", "", "verb", "", "noun_phrase"], lambda n1, s1, v, s2, n2: flatten_values(["<", n1, "> performs the action ", v, " to <", n2, ">"])),
  rule("noun_phrase", ["noun"]),
  rule("noun_phrase", ["adjective", "", "noun"], lambda a, s, n: [n, " with property ", a]),
  rule("noun_phrase", ["noun_phrase","", "noun_phrase","", "verb"], lambda n1, s1, n2, s2, v: ["<", n1, "> which is ", v, "'d by <", n2, ">"]),
  rule("noun", ["buffalo"]),
  rule("verb", ["buffalo"]),
  rule("adjective", ["buffalo"]),
  rule("",["space"])
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