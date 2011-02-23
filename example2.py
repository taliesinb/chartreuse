#!/usr/bin/python

from compiler import *
from chart import *
from rules import *
from patterns import *
from utils import *

def integer(n):
  return symbol("integer", n, (0,0))

def in_sequence(tokens):
  for i in range(len(tokens)):
    t = tokens[i]
    if type(t) == str:
      tokens[i] = symbol(t, t, (i,i+1))
  return tokens
  
rules = [
  rule("start", ["sentence"]),
  rule("medium_query", bag(
    medium="medium", 
    entity_clause=["medium_verb", opt("prep"), "entity"], 
    time_clause=alt("from", "during", "at", "when"),
    about_clause=["about", "topic"])),
    
  rule("sentence", ["medium_query"]),
  rules("time_unit", ["weeks", "days", "hours"]),  
  rule("time_point", ["integer", "time_unit", "ago"]),
  rules("time_span", [["before", "time_point"], ["between", "time_point", "and", "timepoint"], ["around", "time_point"]]),
  
  # tokens:
  rule("medium", ["email", "text", "im"]),
  rule("entity", ["alice", "bob"]),
  rule("medium_verb", ["between", "to", "from"]),
  rule("topic", ["concert", "rent", "movie"])
]

tokens = in_sequence(["emails", "to", "bob", "about", "movie"])

con = context()
con.compile(flatten(rules))

compiled_rules = con.get_rules()

ch = chart(tokens, compiled_rules)

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