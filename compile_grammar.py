#!/usr/bin/python
from collections import defaultdict
from itertools import combinations, groupby

rules = defaultdict(list)
names = defaultdict(int)

# create a new unique name based on original name
def new_name(name):
  names[name] += 1  
  return name + "" + str(names[name])
  
def tostr(arg):
  if type(arg) in [list, tuple]:
    return ''.join(map(tostr, arg))
  else:
    return str(arg)
  
def join_name(*names):
  return  ''.join(map(tostr, names))

# is this term an optional term (= a singleton tuple)
def optionalQ(term):
  return type(term) == tuple and len(term) == 1
  
from itertools import groupby

# handle a term that is a list of consecutive clauses
def dolist(terms, name):
  rules[name] = [[doterm(symbol, new_name(name)) for symbol in terms]]
  return name

# handle a term that is a list of alternative clauses      
def doalt(terms, name):
  for term in terms:
    rules[name].append(term)
  return name
  
def doopt(term, name):
  rules[name] = [[], doterm(term, name)]
  return name

# handle a term that is a bag-of-clauses, returning its name
def dobag(terms, name):
  length = len(terms)
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
      
  rhs = [doterm(symbol, new_name(name)) for symbol in terms.keys()]
  
  for unit_name, term in zip(unit_names, rhs):
    rules[unit_name].append(term)
    
  valid_super_names.append(join_name(name, "0"))
  rules[name] = valid_super_names
  return name
        
# dispatch on a term according to its type
def doterm(term, name):
  t = type(term)
  if t == list:
    return dolist(term, name + "L")
  if t == tuple:
    if len(term) == 1:
      return doopt(term[0], name + "?")
    else:
      return doalt(term, name + "A")
  if t == dict:
    return dobag(term, name + "B")
  if t == str:
    return term
         
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

# test a fixed list containing various other types of clauses
expr = ["a", {"j1":"foo", "j2":"bar", "j3":"baz"}, ["c","d"], ("e","f"), ("g",), "h","i", (["j1","j2"],)]
expr = ["one","1.5","1.6","1.7", ("two?",), ("2.5?",), "three", "four", (["five1","five2"],)]
dolist(expr, "start")

print expr
print

optimize()

print
print "rules:"
for n, r in sorted(rules.items()):
  print "\t", n.ljust(20), r
