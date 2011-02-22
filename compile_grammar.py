#!/usr/bin/python
from collections import defaultdict
from itertools import combinations, groupby

rules = defaultdict(list)
names = defaultdict(int)

def tosym(x):
  if type(x) == str:
    return symbol(x)
  else:
    return x
    
def tosyms(exps):
  return map(tosym, exps)
    
def tostr(arg):
  if type(arg) in [list, tuple]:
    return ''.join(map(tostr, arg))
  else:
    return str(arg)

def next_name(name):
  names[name] += 1
  return join_name(name, names[name])
  
def join_name(*names):
  return  ''.join(map(tostr, names))
  
class symbol:
  def __init__(self, name):
    self.name = name
    
  def compile(self, name):
    return self.name

class seq:
  def __init__(self, *args):
    self.terms = tosyms(args)
    
  def compile(self, name):
    name += "S"
    rules[name] = [[term.compile(next_name(name)) for term in self.terms]]
    return name

class alt:
  def __init__(self, *opts):
    self.terms = tosyms(opts)
        
  def compile(self, name):
    name += "A"
    rules[name] = [term.compile(next_name(name)) for term in self.terms]
    return name
  
class opt:
  def __init__(self, term):
    self.term = tosym(term)

  def compile(self, name):
    name += "?"
    rules[name] = ["_empty_", self.term.compile(name)]
    return name
    
class bag:
  def __init__(self, **args):
    self.terms = tosyms(args)
    
  def compile(self, name):
    name += "B"
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
        rules[super_name] = map(list, list(sub_rules))
        
    rhs = [term.compile(name) for symbol in terms.keys()]
    
    for unit_name, term in zip(unit_names, rhs):
      rules[unit_name].append(term)
      
    valid_super_names.append(join_name(name, "0"))
    rules[name] = valid_super_names
    return name
        
# recursively replace all instances in a list-tree according to dictionary "reps"
def replace_in_list(x, reps):
  if type(x) == list:
    return [replace_in_list(e,reps) for e in x]
  else:
    return reps.get(x,x)

# rewrite rules according to a dictionary, replace every instance of symbol key with symbol value
def rewrite_rules(dict):
  for key in rules:
    if key not in dict:
      rules[key] = replace_in_list(rules[key], dict)
  for key in dict:
    if key in rules:
      del rules[key]
    
# remove redundant rules
def optimize():
  rewrite = {}
  items = list(sorted(rules.items()))
  length = len(items)
  for i in range(length-1):
    name1 = items[i][0]
    for j in range(i+1, length):
      name2 = items[j][0]
      if items[i][1] == items[j][1]:
        rewrite[name2] = name1
        rewrite_rules(rewrite)

  for sym, pattern in rules.items():
    if type(pattern) == list and len(pattern) == 1 and type(pattern[0]) == str:
        rewrite[sym] = pattern[0]
        rewrite_rules(rewrite)
        
  if len(rewrite):
    print "optimization:"
    for a,b in rewrite.items():
      print "\t", a.ljust(20), "->", b

def define(name, expr):
  rules[name].append(expr.compile(name))

# test a fixed list containing various other types of clauses
expr = seq("a", "b", seq("c", "d"), opt("e"), "g", "h")
define("start", expr)

print expr
print

optimize()

print
print "rules:"
for n, r in sorted(rules.items()):
  print "\t", n.ljust(20), r
