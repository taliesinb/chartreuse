#!/usr/bin/python

from collections import defaultdict
from rules import rule, identity

class symbol(object):
  def __init__(self, type, value, span):
    self.type = type
    self.value = value
    self.span = span
    
  def __repr__(self):
    return str(self.value)
    return str(self.value) + " " + str(self.span[0]) + ":" + str(self.span[1])    
    
def flatten_values(x):
  if type(x) == symbol:
    x = x.value
  if type(x) in [list, tuple]:
    return ''.join(map(flatten_values, x))
  else:
    return str(x)

def fake_tokenize(symbols, values):
  n = len(values)
  return map(lambda x,y,z: symbol(x, y, (z,z+1)), symbols, values, range(n))
    
def copy_fragment(frag):
  return fragment(frag.chart, frag.span, frag.pattern, frag.action, frag.matched, frag.type)
  
def new_fragment(chart, pos, rule):
  return fragment(chart, [pos,pos], rule.pattern, rule.action, [], rule.symbol)

class fragment(object):    
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
      if callable(self.action):
        value = self.action(*self.matched)
      else:
        value = self.action
      self.chart.add_symbol(symbol(self.type, value, self.span))
      #print "finished", self.type, "by matching", [m.type for m in self.matched]
  
  def __repr__(self):
    return self.type.ljust(15) + "->" + (' '.join(map(lambda x: str(x.type), self.matched)) + ' | ' + ' '.join(map(str,self.pattern))).strip() + '\t\t' + ','.join(map(lambda x: str(x.value),self.matched))
    return "<" + ','.join(map(str, [self.type, self.span, self.matched])) + '>'
    
  def __hash__(self):
    return hash(self.type) + sum(map(hash, self.matched)) + hash(self.span[0]) + hash(self.span[1])
    
  def __eq__(self, other):
    return self.type == other.type and self.span == other.span and self.matched == other.matched
              
# edge 
class chart(object):
  def __init__(self, tokens, rules):
    self.symbols = defaultdict(set)
    self.edges = defaultdict(set)
    self.rules = defaultdict(list)
    self.rules["_empty_"].append(rule("_empty_", []))
    for r in rules:
      self.rules[r.symbol].append(r)
    self.predict(0, "start")
    
  def parse(self, tokens):
    rightmost = max(t.span[1] for t in tokens)
    for token in tokens:
      self.add_symbol(token)
    winners = [symbol 
      for symbol in self.symbols[(0, "start")] 
      if symbol.span[1] == rightmost]
    return winners
        
  def add_edge(self, frag):
    type = frag.next_type()
    pos = frag.next_pos()
    self.edges[(pos,type)].add(frag)
    for symbol in self.symbols[(pos,type)]:
      copy_fragment(frag).grow(symbol)
    
  def predict(self, pos, type):
    for rule in self.rules.get(type,{}):
      first = rule.first_symbol()
      predict = (pos, first) not in self.edges
      self.add_edge(new_fragment(self, pos, rule))
      if predict:        
        self.predict(pos, first)
  
  def add_symbol(self, symbol):
    #print "adding symbol", symbol.type, "at", symbol.span
    key = (symbol.span[0], symbol.type)
    self.symbols[key].add(symbol)
    for frag in self.edges[key]:
      #print "symbol triggered edge:\t", frag
      copy_fragment(frag).grow(symbol) 
      
  def print_edges(self):
    prefix = "\n    "
    for pos, edge in sorted(self.edges.items()):
      if edge: 
        print pos, prefix, (prefix + " ").join(map(str,edge))
        print

  def print_symbols(self):
    for key, symbol in sorted(self.symbols.items()):
      print str(key).ljust(20)
      for sym in symbol:
        print  "\t\t", str(sym)
        
  def print_rules(self):
    for r in reversed(sorted(self.rules.values())):
      for k in r:
        print k
    

  
    