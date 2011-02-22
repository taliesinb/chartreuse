#!/usr/bin/python
from collections import defaultdict
from itertools import combinations

rules = defaultdict(list)
names = defaultdict(int)

# create a new unique name based on original name
def new_name(name):
  names[name] += 1  
  return name + "_" + str(names[name])

# is this term an optional term (= a singleton tuple)
def optionalQ(term):
  return type(term) == tuple and len(term) == 1
  
# handle a term that is a list of consecutive clauses
def dolist(terms, name):
  rules[name].append(dolist_recurse(terms, name))
  return name
  
def dolist_recurse(terms, name):
  #print "dolist on", terms
  if len(terms) == 0: 
    return []
  term_name = new_name(name)
  if optionalQ(terms[0]):
    rules[term_name].append(dolist_recurse([terms[0][0]] + terms[1:], name))
    rules[term_name].append(dolist_recurse(terms[1:], name))
    return [term_name]
  else:
    return [doterm(terms[0], term_name)] + dolist_recurse(terms[1:], name)

# handle a term that is a list of alternative clauses      
def doalt(terms, name):
  for term in terms:
    rules[name].append(term)
  return name
  
# make a string out of a list of ints
def intstr(ints):
  return ''.join(map(str, sorted(ints)))

# handle a term that is a bag-of-clauses, returning its name
def dobag(terms, name):
  items = terms.items()
  length = len(terms)
  subsets = []
  for i in range(2, length+1):
    for perm in combinations(range(length), i):
      name2 = name + "_" + intstr(perm)
      if 0 in perm:
        subsets.append(name2)
      sub = set()
      for k in range(length):
        if k in perm:
          without = name2.replace(str(k), "")
          below = list(perm)
          below.remove(k)
          suffix = name + "_" + intstr(below)
          sub.add((suffix, name + "_" + str(k)))
          sub.add((name + "_" + str(k), suffix))
      rules[name2] = map(list, list(sub))
      
  rhs = [doterm(item[1], new_name(name)) for item in items]
  
  for i in range(length):
    name2 = name + "_" + str(i)
    rules[name2].append(rhs[i])
    
  subsets.append(name + "_0")
  rules[name] = subsets
  return name
        
# dispatch on a term according to its type
def doterm(term, name):
  t = type(term)
  if t == list:
    return dolist(term, name + "_list")
  if t == tuple:
    return doalt(term, name + "_alts")
  if t == dict:
    return dobag(term, name + "_bag")
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
dolist(["a", {"j1":"foo", "j2":"bar", "j3":"baz"}, ["c","d"], ("e","f"), ("g",), "h","i"], "start")

optimize()

print
print "rules:"
for n, r in sorted(rules.items()):
  print "\t", n.ljust(20), r
