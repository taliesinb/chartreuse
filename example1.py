#!/usr/bin/python

from chart_parser import *
from parser_rule import *

tokens = [
  symbol("buffalo", "Buffalo-born", (0,1)),
  symbol("buffalo", "Bison",        (1,2)),  
  symbol("buffalo", "Buffalo-born", (2,3)),
  symbol("buffalo", "Bison",        (3,4)),
  symbol("buffalo", "bully",        (4,5)),
  symbol("buffalo", "bully",        (5,6)),
  symbol("buffalo", "Buffalo-born", (6,7)),
  symbol("buffalo", "Bison",        (7,8))
]
    
rules = [
  rule("start", ["sentence"]),
  rule("sentence", ["noun_phrase", "verb", "noun_phrase"], lambda n1, v, n2: flatten_values(["<", n1, "> performs the action ", v, " to <", n2, ">"])),
  rule("noun_phrase", ["noun"]),
  rule("noun_phrase", ["adjective", "noun"], lambda a, n: [n, " with property ", a]),
  rule("noun_phrase", ["noun_phrase", "noun_phrase", "verb"], lambda n1, n2, v: ["<", n1, "> which is ", v, "'d by <", n2, ">"]),
  rule("noun", ["buffalo"]),
  rule("verb", ["buffalo"]),
  rule("adjective", ["buffalo"])
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