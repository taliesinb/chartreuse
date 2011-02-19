# chart associates a position with callback
# every time a there is a new symbol-edge in the chart, any callbacks associated with that position
# are called. what they should do is verify that the new symbol is interesting, and if it is,
# generate a new symbol
chartl = {}
chartr = {}

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
  def __init__(self, pattern):
    self.matchs = set()
    self.pattern = pattern
    self.len = len(self.pattern)
    
  def matched(n): # the n'th term got matched
    self.matches.add(n)
    r = n + 1
    l = n - 1
    if r not in self.matches:
      while r < len:
        chart.add(self, pattern[r], r)
        if not pattern[r].optional:
          break
    if l not in self.matches:
      while l >= 0:
        chart.add(self, pattern[l], l)
        if not pattern[l].optional:
          break
    
d
  
        
        
  
    
  
    