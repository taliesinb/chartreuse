from utils import list_replace, identity

def singleton(x):
  if type(x) not in [list]:
    return [x]
  else:
    return x

def rules(symbol, patterns, action=identity):
  return [rule(symbol, singleton(p), action) for p in patterns]

class rule(object):
  def __init__(self, symbol, pattern, action=identity):
    self.symbol = symbol
    if type(pattern) == str: pattern = [pattern]
    self.pattern = pattern
    self.action = action
  
  def first_symbol(self):
    return self.pattern[0]
  
  def replace(self, reps):
    if self.symbol in reps:
      del self # is this okay?
    else:
      list_replace(self.pattern, reps)
      
  def __repr__(self):
    return self.symbol.ljust(15) + "->\t" + str(self.pattern).ljust(20)
  
