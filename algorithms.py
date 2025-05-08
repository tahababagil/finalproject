from toptree import Tree
from parser import parse_dimacs_maxflow
from kruskal import kruskal_minimum_spanning_forest
import time
from naive import DynamicMST
import sys
tree = Tree()
set_ = set()
fn = sys.argv[1]

edges_ = parse_dimacs_maxflow(fn)
set_ = set()
edges = []
edges_k = []

times = []
for u,v,c in edges_:
    if (str(u),str(v)) in set_ or (str(v),str(u)) in set_:
        continue
    set_.add((str(u),str(v)))
    edges.append((u,v,c))
    edges_k.append((u.name,v.name,c))


start = time.time()
for u,v,c in edges:
    C = tree.expose(u,v)
    if C is None:
        tree.link(u,v,c)
    elif C.data.max_cost > c:
        tree.cut(C.data.ptr)
        tree.link(u,v,c)
end = time.time()

times.append([0,0,0])
times[-1][0] = end-start
start = time.time()
f = kruskal_minimum_spanning_forest(edges_k)
end = time.time()
times[-1][1] = end-start
start = time.time()
dynamic_mst = DynamicMST()
for u, v, c in edges_k:
    updated = dynamic_mst.add_edge(u, v, c)

end = time.time()
times[-1][2] = end-start
print(f"""
    filename: {fn}
    Time to run toptree: {times[0][0]}
    Time to run kruskal offline: {times[0][1]}
    Time to run naive algorithm: {times[0][2]}
    # Sum for toptree: {sum(sum(a.cluster.data.max_cost for a in r.get_levels()[-1]) for r in tree.roots)}
    # Sum for kruskal: {sum(x for _,_,x in f)}
    # Sum for naive:  {sum(x for _,_,x in dynamic_mst.get_mst_edges())}
    """)