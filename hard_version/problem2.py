from collections import defaultdict
from itertools import chain

def farthest_nodes(strArr):

  # Reshapping input to get rid of the '-'
  edges = [[path.split('-')[0], path.split('-')[1]] for path in strArr]

  # Create a default dict with all connected nodes per node
  G = defaultdict(list)
  for (s,t) in edges:
    G[s].append(t)
    G[t].append(s)
  
  # Use a depth-first search algorithm to discover all paths
  def DFS(G, v, seen=None, path=None):
    if seen == None:
      seen = []
    if path == None:
      path = []
    
    seen.append(v)

    paths = []
    for t in G[v]:
      if t not in seen:
        t_path = path + [t]
        paths.append(tuple(t_path))
        paths.extend(DFS(G, t, seen[:], t_path))
    
    return paths

  #Run DFS, compute metrics
  all_paths = list(chain.from_iterable(DFS(G, n) for n in set(G)))
  max_len = max(len(p) for p in all_paths)

  # code goes here
  return max_len

# keep this function call here 
print(farthest_nodes(input()))

# Example input: inp = ["b-e","b-c","c-d","a-b","e-f"]
