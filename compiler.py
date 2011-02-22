#!/usr/bin/python
from collections import defaultdict
from itertools import combinations, groupby
from rules import rule
from utils import flatten, identity, stringify, first
      
def join_name(*names):
  return  ''.join(map(stringify, names))

class context(object):
  def __init__(self):
    self.rules = defaultdict(list)
    self.names = defaultdict(int)

  def compile(self, rules):
    for r in rules:
      r.pattern.set_context(self)
      name = r.pattern.compile(r.symbol)
      if name != r.symbol:
        self.rules[r.symbol].append(rule(r.symbol, [name], identity))
      
  def optimize(self):
    rewrite = {}
    items = list(sorted(self.rules.items()))
    length = len(items)
    for sym1, list1 in range(length-1):
      name1 = items[i][0]
      for j in range(i+1, length):
        name2 = items[j][0]
        if items[i] == items[j]:
          rewrite[name2] = name1
          rename_symbol(rewrite)
  
    for sym, rulelist in items:
      if len(rulelist) == 1:
        only = rulelist[0]
        if type(only) == str:
          rewrite[sym] = only
          rename_symbol(rewrite)
        elif type(only) == list and len(only) == 1 and type(only[0]) == str:
          rewrite[sym] = only[0]
          rename_symbol(rewrite)
          
    if len(rewrite):
      print "optimization:"
      for a,b in rewrite.items():
        print "\t", a.ljust(20), "->", b

  def rename_symbol(self, reps):
    for symbol, rulelist in rules:
      for i in range(len(rulelist)):
        rules[symbol][i].rewrite(reps)
        
  def print_rules(self):
    for r in reversed(sorted(self.rules.values())):
      for k in r:
        print k
