#!/usr/bin/python
from copy import copy
from collections import defaultdict
from sys import setrecursionlimit

setrecursionlimit(64)

class symbol:
  def __init__(self, type, value):
    self.type = type
    self.value = value
    
  def __repr__(self):
    return str(self.value)

def copy_fragment(frag):
  return fragment(frag.chart, frag.left, frag.right, frag.remaining, frag.matched, frag.type)
  
def new_fragment(chart, pos, type, symbols):
  return fragment(chart, pos, pos, symbols, [], type)

class fragment:    
  def __init__(self, chart, left, right, remaining, matched, type):
    self.chart = chart
    self.left = left
    self.right = right
    self.remaining = copy(remaining)
    self.matched = copy(matched)
    self.type = type
    
  def next_type(self):
    return self.remaining[0]
    
  def next_pos(self):
    return self.right
                
  def grow(self, sym, pos):
    print "fragment of type", self.type, "growing using symbol", sym.type
    assert self.right == pos[0]
    assert self.remaining
    assert sym.type == self.remaining.pop(0)
    self.matched.append(sym)
    self.right = pos[1]
    if self.remaining: 
      self.chart.add_edge(self)
      self.chart.predict(self.next_pos(), self.next_type())
    else:
      match = self.matched
      if len(match) == 1: 
        match = match[0]
      self.chart.add_symbol((self.left, self.right), symbol(self.type, match))
      print "finished", self.type, "by matching", [m.type for m in self.matched]
          
# edge 
class chart:
  def __init__(self, tokens, rules):
    self.symbols = defaultdict(set)
    self.edges = defaultdict(set)
    self.rules = rules
    self.predict(0, "start")
    print "prediction finished, adding symbols"
    print
    for (l, r, sym) in tokens:
      self.add_symbol((l,r), sym)
    
  def add_edge(self, frag):
    print "adding edge for:", frag.type, "at", frag.next_pos(), "on", frag.next_type()
    type = frag.next_type()
    pos = frag.next_pos()
    self.edges[(pos,type)].add(frag)
    for symbol in self.symbols[(pos,type)]:
      copy_fragment(frag).grow(symbol, pos)
    
  def predict(self, pos, type):
    for rule in rules.get(type,[]):
      print "predicting fragment", "'" + type + "'", "at", pos, "via", rule
      predict = (pos, rule[0]) not in self.edges
      
      self.add_edge(new_fragment(self, pos, type, rule))
      if predict:        
        self.predict(pos, rule[0])
      else:
        print (pos, rule[0]), "is already in edges"
  
  def add_symbol(self, pos, symbol):
    print "adding symbol", symbol.type, "at", pos
    key = (pos[0], symbol.type)
    self.symbols[key].add(symbol)
    for frag in self.edges[(pos[0], symbol.type)]:
      print "symbol triggered edge"
      copy_fragment(frag).grow(symbol, pos) 
    
tokens = [
  (0,1, symbol("a", "A1")),
  (1,2, symbol("a", "A2")),  
  (2,3, symbol("a", "A3")),
  (3,4, symbol("a", "A4")),
  (4,5, symbol("b", "B"))]
  
rules = {}
rules["start"] = [["A", "b"]]
rules["A"] = [["A", "A"], ["a"]]

ch = chart(tokens, rules)
print
if (0, "start") in ch.symbols:
  print "winning symbols:"
  for win in ch.symbols[(0, "start")]:
    print win
else:
  print "full chart:"
  for key, symbol in ch.symbols.items():
    print key[0], " -> ", symbol

print "done"

# artisan asylum: tuesday
# sprout: thursday      
    

  
    