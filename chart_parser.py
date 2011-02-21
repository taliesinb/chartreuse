#!/usr/bin/python
from collections import defaultdict
from sys import setrecursionlimit

setrecursionlimit(64)

class symbol:
  def __init__(self, type, value, span):
    self.type = type
    self.value = value
    self.span = span
    
  def __repr__(self):
    return str(self.value)

def copy_fragment(frag):
  return fragment(frag.chart, frag.span, frag.pattern, frag.action, frag.matched, frag.type)
  
def new_fragment(chart, pos, type, pattern, action):
  return fragment(chart, [pos,pos], pattern, action, [], type)

class fragment:    
  def __init__(self, chart, span, pattern, action, matched, type):
    self.chart = chart
    self.span = span[:]
    self.action = action
    self.pattern = pattern[:]
    self.matched = matched[:]
    self.type = type
    
  def next_type(self):
    return self.pattern[0]
    
  def next_pos(self):
    return self.span[1]
                
  def grow(self, sym):
    #print "fragment of type", self.type, "growing using symbol", sym.type
    assert self.next_pos() == sym.span[0]
    assert self.pattern
    assert sym.type == self.pattern.pop(0)
    self.matched.append(sym)
    self.span[1] = sym.span[1]
    if self.pattern: 
      self.chart.add_edge(self)
      self.chart.predict(self.next_pos(), self.next_type())
    else:
      self.chart.add_symbol(symbol(self.type, self.action(*self.matched), self.span))
      #print "finished", self.type, "by matching", [m.type for m in self.matched]
  
  def __repr__(self):
    return self.type + ":\t" + (' '.join(map(lambda x: str(x.type), self.matched)) + ' | ' + ' '.join(map(str,self.pattern))).strip() + '\t\t' + ','.join(map(lambda x: str(x.value),self.matched))
    return "<" + ','.join(map(str, [self.type, self.span, self.matched])) + '>'
    
  def __hash__(self):
    return hash(self.type) + sum(map(hash, self.matched)) + hash(self.span[0]) + hash(self.span[1])
    
  def __eq__(self, other):
    return self.type == other.type and self.span == other.span and self.matched == other.matched
              
# edge 
class chart:
  def __init__(self, tokens, rules):
    self.symbols = defaultdict(set)
    self.edges = defaultdict(set)
    self.rules = rules
    self.predict(0, "start")
    
  def parse(self, tokens):
    rightmost = max(t.span[1] for t in tokens)
    for token in tokens:
      self.add_symbol(token)
    winners = [symbol 
      for symbol in ch.symbols[(0, "start")] 
      if symbol.span[1] == rightmost]
    return winners
        
  def add_edge(self, frag):
    #print "adding edge for:", frag.type, "at", frag.next_pos(), "on", frag.next_type()
    type = frag.next_type()
    pos = frag.next_pos()
    self.edges[(pos,type)].add(frag)
    for symbol in self.symbols[(pos,type)]:
      copy_fragment(frag).grow(symbol)
    
  def predict(self, pos, type):
    for pattern, action in rules.get(type,{}):
      #print "predicting fragment", "'" + type + "'", "at", pos, "via pattern", pattern
      first_symbol = pattern[0]
      predict = (pos, first_symbol) not in self.edges
      self.add_edge(new_fragment(self, pos, type, pattern, action))
      if predict:        
        self.predict(pos, first_symbol)
  
  def add_symbol(self, symbol):
    #print "adding symbol", symbol.type, "at", symbol.span
    key = (symbol.span[0], symbol.type)
    self.symbols[key].add(symbol)
    for frag in self.edges[key]:
      #print "symbol triggered edge:\t", frag
      copy_fragment(frag).grow(symbol) 
      
  def print_edges(self):
    for pos, edge in sorted(ch.edges.items()):
      if edge: 
        print pos, "\n\t", '\n\t'.join(map(str,edge))

  def print_symbols(self):
    for key, symbol in ch.symbols.items():
      print key, "\t->\t", symbol
    
    
tokens = [
  symbol("a", "A1", (0,1)),
  symbol("a", "A2", (1,2)),  
  symbol("a", "A3", (2,3)),
  symbol("b", "B1", (3,4)),
  symbol("b", "B2", (4,5))
]
  
rules = {}
rules["start"] = [(["A", "B"], lambda x, y: (x,y))]
rules["A"] = [(["A", "A"], lambda x, y: (x,y)), (["a"], lambda x: "a")]
rules["B"] = [(["a", "b", "b"], lambda x, y, z: (x,y,z)), (["b"], lambda x: "b")]

ch = chart(tokens, rules)

winners = ch.parse(tokens)

print "winners:"
for w in winners:
  print "\t", winners

if winners:  
  print
  print "chart:"
  ch.print_symbols()

  print
  print "edges:"
  ch.print_edges()

# artisan asylum: tuesday
# sprout: thursday      
    

  
    