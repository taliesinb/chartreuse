# chart associates a position with callback
# every time a there is a new symbol-edge in the chart, any callbacks associated with that position
# are called. what they should do is verify that the new symbol is interesting, and if it is,
# generate a new symbol
rules = [
  ([1,2], 1),
  ([1,3], 3)
]

# in the first round, all tokens are examined in turn
# each token might occur as a trigger for one or more rules
# these triggers then register callbacks on their left and right that
# on being called will build a bigger match

# it would be great if partial matches were just closures
# i don't think that can be the case, though, because a partial needs
# multiple callbacks. it must say: I am interested in being extended
# on the left *and* on the right

# how many kinds of partials? 
# fixed orders, with any terms inside being optional
# repeated, with a 'riffle' that they are allowed to pick up between items

# now what if the optional terms are also perhaps identical to the fixed terms?
# then we can extend in multiple ways. we should clone ourself and grow both
# so while we could be given a new token and asked: 'how do you want to grow'?
# it might make more sense to just be asked: what could you match on the left
# and right? and for it to then lay down triggers on the left and right

def term:
  def __init__(self, symbols, optional):
    self.optional = optional
    self.symbols = symbols
    
  def is_match(self, symbol):
    return symbol in self.symbols

class partial:
  def __init__(self, pos, terms):
    self.matchs = set()
    self.terms = terms
    self.l_pos = {}
    self.r_pos = {}
    self.len = len(self.terms)
    self.children = []
    
  def __init__(self, other):
    self.matches = other.matches
    self.terms = other.terms
    self.l_pos = other.l_pos
    self.r_pos = other.r_pos
    self.len = other.len
    self.children = []
    
  def clone(self):
    child = partial(self)
    self.children.append(child)
    
  def satisfied(self):
    for i in range(len):
      if i not in self.matches and not i.optional:
        return false
      return true
    
  def matched(self, n): # the n'th term got matched
    self.matches.add(n)
    r = n + 1
    l = n - 1
    if r not in self.matches:
      while r < len:
        chart.add_r_trigger(self, r_pos[r], self, r)
        if not terms[r].optional:
          break
          
    if l not in self.matches:
      while l >= 0:
        chart.add_l_trigger(self, l_pos[l], self, l)
        if not terms[l].optional:
          break
          
# trigger 
class chart:
  def __init__(self, symbols):
    self.l_symbols = {}
    self.r_symbols = {}
    for (sym, l, r) in symbols:
      self.add_l_symbol(l, sym)
      self.add_r_symbol(r, sym)
    self.l_triggers = {}
    self.r_triggers = {}
    
  def add_l_trigger(self, pos, partial, n):
    self.l_triggers[pos] = (partial, n)
  
  def add_r_trigger(self, pos, partial, n):
    self.r_triggers[pos] = (partial, n)
        
  def add_l_symbol(self, pos, partial):
    pass.l_symbols[pos] = partial
  
  def add_r_symbol(self, pos, sym):
    pass.r_symbols[pos] = partial
    
    
        
        
  
    
  
    