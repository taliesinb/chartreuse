#!/usr/bin/python
from collections import defaultdict
from itertools import combinations, groupby
from parser_rule import rule
from utils import flatten, identity, stringify, first

def tosym(x):
  if type(x) == str:
    return symbol(x)
  else:
    return x
    
def tosyms(exps):
  return map(tosym, exps)
      
def join_name(*names):
  return  ''.join(map(stringify, names))

class context(object):
  def __init__(self):
    self.rules = defaultdict(list)
    self.names = defaultdict(int)

  def compile(self, rules):
    for r in rules:
      r.pattern.set_context(self)
      name = r.pattern.compile(r.symbol)
      if name != r.symbol:
        self.rules[r.symbol].append(rule(r.symbol, [name], identity))
      
  def optimize(self):
    rewrite = {}
    items = list(sorted(self.rules.items()))
    length = len(items)
    for sym1, list1 in range(length-1):
      name1 = items[i][0]
      for j in range(i+1, length):
        name2 = items[j][0]
        if items[i] == items[j]:
          rewrite[name2] = name1
          rename_symbol(rewrite)
  
    for sym, rulelist in items:
      if len(rulelist) == 1:
        only = rulelist[0]
        if type(only) == str:
          rewrite[sym] = only
          rename_symbol(rewrite)
        elif type(only) == list and len(only) == 1 and type(only[0]) == str:
          rewrite[sym] = only[0]
          rename_symbol(rewrite)
          
    if len(rewrite):
      print "optimization:"
      for a,b in rewrite.items():
        print "\t", a.ljust(20), "->", b

  def rename_symbol(self, reps):
    for symbol, rulelist in rules:
      for i in range(len(rulelist)):
        rules[symbol][i].rewrite(reps)
  
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

class symbol(pattern):
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

# test a fixed list containing various other types of clauses
expr = seq("a", "b", seq("c", "d"), opt("e"), "g", "h")
expr = bag(a="aye", b="bee", c="see")

c = context()

rules = [
  rule("start", seq("a", opt("b1", "b2"), "c"), identity),
  rule("start", bag(a="A", b="B", c="C"), identity)
]

c.compile(rules)

print expr
print

#optimize()

print
print "rules:"
for r in reversed(sorted(c.rules.values())):
  for k in r:
    print k
