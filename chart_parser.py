#!/usr/bin/python
from copy import copy
from collections import defaultdict

class symbol:
  def __init__(self, type, value):
    self.type = type
    self.value = value
    
  def __repr__(self):
    return "(" + self.type + ":" + str(self.value) + ")"

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
    print "fragment of type", self.type, "growing using symbol", sym.type, "into remaining", self.remaining
    assert self.right == pos[0]
    assert self.remaining
    print sym.type, "==", self.remaining[0]
    assert sym.type == self.remaining.pop(0)
    self.matched.append(sym)
    self.right = pos[1]
    if self.remaining: 
      self.chart.add_edge(self)
      self.chart.predict(self.next_pos(), self.next_type())
    else:
      self.chart.add_symbol((self.left, self.right), symbol(self.type, self.matched))
      print "finished", self.type, "by matching", [m.type for m in self.matched]
          
# edge 
class chart:
  def __init__(self, tokens, rules):
    self.symbols = defaultdict(list)
    self.edges = defaultdict(list)
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
    self.edges[(pos,type)].append(frag)
    for symbol in self.symbols[(pos,type)]:
      copy_fragment(frag).grow(symbol, pos)
    
  def predict(self, pos, type):
    for rule in rules.get(type,[]):
      print "predicting fragment", type, "at", pos, "via", rule
      self.add_edge(new_fragment(self, pos, type, rule))
  
  def add_symbol(self, pos, symbol):
    print "adding symbol", symbol.type, "at", pos
    key = (pos[0], symbol.type)
    self.symbols[key].append(symbol)
    for frag in self.edges[(pos[0], symbol.type)]:
      print "symbol triggered edge"
      copy_fragment(frag).grow(symbol, pos) 
    
tokens = [
  (0,2, symbol("a", "A")),
  (2,3, symbol("b", "good b")),
  (2,5, symbol("b", "bad b")),
  (3,5, symbol("c", "C"))]
rules = {}
rules["start"] = [["a", "b", "c"], ["c","b","a"]]
rules["middle"] = [["a", "end", "c"]]
rules["end"] = [["b"], ["bb"]]

ch = chart(tokens, rules)

for key, symbol in ch.symbols.items():
  print key, " -> ", symbol

print "done"

# artisan asylum: tuesday
# sprout: thursday      
    

  
    