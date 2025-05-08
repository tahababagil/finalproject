def kruskal_minimum_spanning_forest(edges):
    parent = {}
    rank = {}
    def find(u):
        if parent[u] != u:
            parent[u] = find(parent[u])
        return parent[u]
    def union(u, v):
        root_u = find(u)
        root_v = find(v)
        if root_u == root_v:
            return False
        if rank[root_u] < rank[root_v]:
            parent[root_u] = root_v
        else:
            parent[root_v] = root_u
            if rank[root_u] == rank[root_v]:
                rank[root_u] += 1
        return True

    for u, v, c in edges:
        if u not in parent:
            parent[u] = u
            rank[u] = 0
        if v not in parent:
            parent[v] = v
            rank[v] = 0

    sorted_edges = sorted(edges, key=lambda x: x[2])
    forest = []
    for u, v, c in sorted_edges:
        if union(u, v):
            forest.append((u, v, c))
    return forest

