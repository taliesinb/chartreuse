class fragment:
  def __init__(self, pos, type, symbols):
    self.right = self.left = pos
    self.remaining = symbols
    self.matched = []
    self.type = type
        
  def grow(self, symbol, pos):
    assert self.right == pos[0]
    assert self.remaining
    assert symbol.type = self.remaining.pop()
    self.matched.append(symbol)
    self.right = pos[1]
    if not self.remaining: 
      self.chart.add_symbol(self, self.left, self.type)
    else:
      self.chart.add_trigger(self, self.right, self.remaining[-1])
          
# trigger 
class chart:
  def __init__(self, symbols, rules):
    self.symbols = {}
    self.rules = {}
    for (l, r, sym) in symbols:
      self.add_symbol(l, sym)
    self.triggers = {}
    
  def add_trigger(self, pos, type, partial):
    self.triggers[(pos, type)] = partial
  
  def add_symbol(self, pos, type, symbol):
    self.symbols[(pos, type)] = symbol
    [t.grow(symbol, pos) for t in self.triggers.get((pos, type), [])
    
ch = chart([(1,2,"a"),(2,3,"b"),(3,4,"c")],
  {"start": [
    ["a","b","c"],
    ["c","b","a"]
  ]})
  
  


      
    

  
    