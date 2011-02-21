#!/usr/bin/python

from collections import defaultdict
from itertools import combinations

"""
what can productions look like?
["a", "b", "c"] means fixed order
{"l":"a", "r":"b", "m":"c"} means an any-order bag, keys and values are stored in dictionary
{"!l": "a"] means that term l has to appear
["a", ("b","c"), "c"] means alternatives
["a", "?b", "c"] means that 'b' is optional
"""

rules = defaultdict(list)
names = defaultdict(int)

def new_name(name):
  names[name] += 1  
  return name + "_" + str(names[name])

def optionalQ(term):
  return type(term) == tuple and len(term) == 1
  
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
      
def doalt(terms, name):
  for term in terms:
    rules[name].append(term)
  return name
  
# {1: "a", 2:"b", 3:"c"}
# make grammar symbol for each pair
# sym12 -> [1,2], [2,1] sym13 -> [1,3],[3,1] sym23 -> [2,3],[3,2]
# sym123 -> [sym[12], 3], [3, sym[12]]

def flatten(lists):
  if type(lists) in [list, tuple]:
    return reduce((lambda x,y: x + y), (flatten(f) for f in lists))
  else:
    return [lists]

def intstr(ints):
  return ''.join(map(str, sorted(ints)))

def dobag(terms, name):
  items = terms.items()
  length = len(terms)
  subsets = []
  for i in range(2, length+1):
    for perm in combinations(range(length), i):
      name2 = name + "_" + intstr(perm)
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
    subsets.append(name2)
    rules[name2].append(rhs[i])
    
  rules[name] = subsets
  return name
        
def doterm(term, name):
  t = type(term)
  if t == list:
    return dolist(term, name + "_list")
  if t == tuple:
    return doalt(term, name + "_alts")
  if t == dict:
    return dobag(term, name)
  if t == str:
    return term
  
# x -> a ?b c
# x -> a b c
# x -> a c
# x -> x_1
# x_1 -> a x_2
# x_2 -> b c
# x_2 -> c
# [a] [?b c]
       
rewrite = {}

def replace_in_list(x, reps):
  if type(x) == list:
    return [replace_in_list(e,reps) for e in x]
  else:
    return reps.get(x,x)

def optimize():
  global rewrite
  rewrite = {}
  items = list(sorted(rules.items()))
  length = len(items)
  for i in range(length-1):
    name1 = items[i][0]
    for j in range(i+1, length):
      name2 = items[j][0]
      if items[i][1] == items[j][1]:
        rewrite[name2] = name1
        del rules[name2]

  for sym, pattern in rules.items():
    if type(pattern) == list and len(pattern) == 1 and type(pattern[0]) == str:
        rewrite[sym] = pattern[0]
        del rules[sym]
        
  if len(rewrite):
    print "optimization:"
  for a,b in rewrite.items():
    print "\t", a.ljust(20), "->", b
  for key in rules:
    rules[key] = replace_in_list(rules[key], rewrite)
       
dobag({1:"a",2:["b","c"],3:"c"}, "start")
#dolist(["a","b","c",,"d","e","f"], "start")

optimize()
print
print "rules:"
for n, r in rules.items():
  print "\t", n.ljust(20), r
