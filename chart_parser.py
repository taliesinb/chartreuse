#!/usr/bin/python

class symbol:
  def __init__(self, type):
    self.type = type
    self.value = None

class fragment:
  def __init__(self, chart, pos, type, symbols):
    self.chart = chart
    self.right = self.left = pos
    self.remaining = symbols
    self.matched = []
    self.type = type
    
  def next_type(self):
    return self.remaining[0]
    
  def next_pos(self):
    return self.right
        
  def grow(self, sym, pos):
    assert self.right == pos[0]
    assert self.remaining
    assert sym.type == self.remaining.pop(0)
    self.matched.append(sym)
    self.right = pos[1]
    if self.remaining: 
      self.chart.add_trigger(self)
      self.chart.predict(next_pos(), next_type())
    else:
      self.chart.add_symbol((self.left, self.right), symbol(self.type))
      print "finished ", self.type, "by matching", self.matched
          
# trigger 
class chart:
  def __init__(self, tokens, rules):
    self.symbols = {}
    self.triggers = {}
    self.rules = rules
    for (l, r, t) in tokens:
      self.add_symbol((l,r), t)
    predict(0, "start")
    
  def add_trigger(self, frag):
    type = frag.next_type()
    pos = frag.next_pos()
    self.triggers.setdefault((pos,type), []).append(fragment)
    
  def predict(self, pos, type):
    for rule in rules.get(type,[]):
      self.add_trigger(fragment(self, pos, type, rule))
  
  def add_symbol(self, pos, symbol):
    self.symbols[(pos, symbol.type)] = symbol
    for t in self.triggers.get((pos[0], symbol.type), []):
      t.grow(symbol, pos) 
    
tokens = [
  (0,2, symbol("a")),
  (2,3, symbol("b")),
  (3,5, symbol("c"))]
rules = {}
rules["start"] = [["a", "b", "c"], ["c","b","a"]]

ch = chart(tokens, rules)

print "done"


# artisan asylum: tuesday
# sprout: thursday      
    

  
    