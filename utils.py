
def flatten(xs):
  f = []
  for x in xs:
    if type(x) == list:
      f += flatten(x)
    else:
      f.append(x) 
  return f

def first(x, *y):
  return x

def identity(*x):
  if len(x) == 1:
    return x[0]
  else:
    return x
    
def stringify(arg):
  if type(arg) in [list, tuple]:
    return ''.join(map(stringify, arg))
  else:
    return str(arg)
    
# recursively replace all instances in a list-tree according to dictionary "reps"
def list_replace(x, reps):
  if type(x) == list:
    return [list_replace(e,reps) for e in x]
  else:
    return reps.get(x,x)
