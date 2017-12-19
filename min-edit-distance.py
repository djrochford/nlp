import numpy as np

def min_edit_distance(source, target):

  del_cost = lambda char: 1
  ins_cost = lambda char: 1
  sub_cost = lambda char_source, char_target: 0 if char_source == char_target else 2

  source = '*' + source
  target = '*' + target

  n = len(source)
  m = len(target)
  distance = np.zeros((n, m), dtype=tuple)

  distance[0,0] = (0, None)
  for i in range(1, n):
    distance[i, 0] = (distance[i-1, 0][0] + del_cost(source[i]), (i-1, 0))
  for j in range(1, m):
    distance[0, j] = (distance[0, j-1][0] + ins_cost(target[j]), (0, j-1))

  for i in range(1, n):
    for j in range(1, m):
      via_deletion = distance[i-1, j][0] + del_cost(source[i])
      via_insertion = distance[i, j-1][0] + ins_cost(target[j])
      via_substitution = distance[i-1, j-1][0] + sub_cost(source[i], target[j])
      minimum = min(via_deletion, via_insertion, via_substitution)
      if minimum == via_substitution:
        distance[i, j] = (via_substitution, (i-1, j-1))
      elif minimum == via_deletion:
        distance[i, j] = (via_deletion, (i-1, j))
      else:
        distance[i, j] = (via_insertion, (i, j-1))

  trace = []
  address = (n-1, m-1)
  while address:
    trace.append(address)
    i, j = address
    previous_i, previous_j = distance[i, j][1]
    if previous_i < i and previous_j < j:
      

  return distance[n-1, m-1][0], trace
  
print(min_edit_distance('intention', 'execution'))
