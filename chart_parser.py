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
  return fragment(frag.chart, frag.left, frag.right, frag.pattern, frag.action, frag.matched, frag.type)
  
def new_fragment(chart, pos, type, pattern, action):
  print "new with pattern", pattern
  return fragment(chart, pos, pos, pattern, action, [], type)

class fragment:    
  def __init__(self, chart, left, right, pattern, action, matched, type):
    self.chart = chart
    self.left = left
    self.right = right
    self.action = action
    self.pattern = copy(pattern)
    self.matched = copy(matched)
    self.type = type
    
  def next_type(self):
    return self.pattern[0]
    
  def next_pos(self):
    return self.right
                
  def grow(self, sym, pos):
    print "fragment of type", self.type, "growing using symbol", sym.type
    assert self.right == pos[0]
    assert self.pattern
    assert sym.type == self.pattern.pop(0)
    self.matched.append(sym)
    self.right = pos[1]
    if self.pattern: 
      self.chart.add_edge(self)
      self.chart.predict(self.next_pos(), self.next_type())
    else:
      self.chart.add_symbol((self.left, self.right), symbol(self.type, self.action(*self.matched)))
      print "finished", self.type, "by matching", [m.type for m in self.matched]
  
  def __repr__(self):
    return self.type + ":\t" + (' '.join(map(lambda x: str(x.type), self.matched)) + ' | ' + ' '.join(map(str,self.pattern))).strip() + '\t\t' + ','.join(map(lambda x: str(x.value),self.matched))
    return "<" + ','.join(map(str, [self.type, self.left, self.right, self.matched])) + '>'
    
  def __hash__(self):
    return hash(self.type) + sum(map(hash, self.matched)) + hash(self.left) + hash(self.right)
    
  def __eq__(self, other):
    return self.type == other.type and self.left == other.left and self.right == other.right and self.matched == other.matched
              
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
    for pattern, action in rules.get(type,{}):
      print "predicting fragment", "'" + type + "'", "at", pos, "via pattern", pattern
      first_symbol = pattern[0]
      predict = (pos, first_symbol) not in self.edges
      self.add_edge(new_fragment(self, pos, type, pattern, action))
      if predict:        
        self.predict(pos, first_symbol)
  
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
  (3,4, symbol("b", "B1")),
  (4,5, symbol("b", "B2"))]
  
rules = {}
rules["start"] = [(["A", "B"], lambda x, y: (x,y))]
rules["A"] = [(["A", "A"], lambda x, y: (x,y)), (["a"], lambda x: "a")]
rules["B"] = [(["a", "b", "b"], lambda x, y, z: (x,y,z)), (["a"], lambda x: "a")]

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

print
print "edges:"
for pos, edge in sorted(ch.edges.items()):
  if edge: 
    print pos, "\n\t", '\n\t'.join(map(str,edge))
  print

print "done"

# artisan asylum: tuesday
# sprout: thursday      
    

  
    