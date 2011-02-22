#!/usr/bin/python

from compiler import *
from chart import *
from rules import *
from patterns import *
from utils import *

tokens = fake_tokenize(
  ["medium", "medium_verb", "prep", "entity"], 
  ["emails", "that I've sent", "to", "johhnie"]
)
  
rules = [
  rule("start", ["sentence"]),
  rule("sentence", ["medium", "medium_verb", "prep", "entity"]),
  rules("time_unit", ["weeks", "days", "hours"]),  
  rule("time_point", ["integer", "time_unit", "ago"]),
  rules("time_span", [["before", "time_point"], ["between", "time_point", "and", "timepoint"], ["around", "time_point"]]),
  rule("medium", ["email", "text", "im"])
]

ch = chart(tokens, flatten(rules))

winners = ch.parse(tokens)

print "rules:"
ch.print_rules()
print
print "symbols:"
ch.print_symbols()

print
print "winners:"

i = 0
for w in sorted(winners):
  print i, "\t", w
  i += 1
  
'''
# test a fixed list containing various other types of clauses
expr = seq("a", "b", seq("c", "d"), opt("e"), "g", "h")
expr = bag(a="aye", b="bee", c="see")

c = context()

rules = [
  rule("start", seq("a", opt("b1", "b2"), "c"), identity),
  rule("start", bag(a="A", b="B", c="C"), identity)
]

c.compile(rules)

c.print_rules()
'''