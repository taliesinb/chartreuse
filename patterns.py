from rules import *
from compiler import *

def singleton(x):
  if type(x) == str or type(x) == pattern:
    return [x]
  else:
    return x

class pattern(object):
  def __init__(self, *terms):
    self.terms = tosyms(terms)
    
  def __iter__(self):
    return iter(self.terms)
    
  def set_context(self, context):
    self.context = context
    for i in self:
      i.set_context(context)

  def next_name(self, name):
    self.context.names[name] += 1
    return join_name(name, self.context.names[name])
    
  def append(self, rule):
    self.context.rules[rule.symbol].append(rule)

def tosym(x):
  if type(x) == str:
    return sym(x)
  else:
    return x
    
def tosyms(exps):
  return map(tosym, exps)

class sym(pattern):
  def __init__(self, name):
    self.name = name
    
  def __iter__(self):
    return iter([])
    
  def compile(self, name):
    return self.name

class seq(pattern):    
  def compile(self, name):
    name += "."
    self.append(rule(name, [term.compile(self.next_name(name)) for term in self], flatten))
    return name

class alt(pattern):        
  def compile(self, name):
    name += "|"
    for term in self:
      self.append(rule(name, [term.compile(self.next_name(name))], first))
    return name
  
class opt(pattern):
  def compile(self, name):
    name += "?"
    self.append(rule(name, "_empty_", first))
    for term in self:
      self.append(rule(name, [term.compile(name)], first))
    return name
    
class bag(pattern):
  def __init__(self, **args):
    self.terms = {}
    for k, v in args.items():
      self.terms[k] = tosym(v)
      
  def __iter__(self):
    return iter(self.terms.values())
    
  def compile(self, name):
    name += ":"
    length = len(self.terms)
    valid_super_names = []
    unit_names = [join_name(name, k) for k in range(length)]

    for i in range(2, length+1):
      for perm in combinations(range(length), i):
        super_name = join_name(name, perm)
        if 0 in perm:
          valid_super_names.append(super_name)
        sub_rules = set()
        for k in range(length):
          if k in perm:
            sub_perm = list(perm)
            sub_perm.remove(k)
            sub_name = join_name(name, sub_perm)
            sub_rules.add((sub_name, unit_names[k]))
            sub_rules.add((unit_names[k], sub_name))
        for k in sub_rules:
          self.append(rule(super_name, k, identity))
        
    rhs = [term.compile(name) for term in self.terms.values()]
    
    for unit_name, term in zip(unit_names, rhs):
      self.append(rule(unit_name, term, first)) 
      
    valid_super_names.append(join_name(name, "0"))
    for super_name in valid_super_names:
      self.append(rule(name, super_name, identity))
    return name
