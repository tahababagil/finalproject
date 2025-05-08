from collections import deque
class DynamicMST:
    def __init__(self):
        self.forest = {}
        self.mst_edges = set()

    def add_edge(self, u, v, w):
        if u not in self.forest:
            self.forest[u] = []
        if v not in self.forest:
            self.forest[v] = []
        if not self.is_connected(u, v):
            self._insert_edge(u, v, w)
            return True
        else:
            path = self.find_path(u, v)
            if path is None:
                return False
            max_edge = None
            max_weight = -float('inf')
            for edge in path:
                if edge[2] > max_weight:
                    max_edge = edge
                    max_weight = edge[2]
            if max_weight > w:
                self._remove_edge(max_edge[0], max_edge[1], max_edge[2])
                self._insert_edge(u, v, w)
                return True
            else:
                return False

    def _insert_edge(self, u, v, w):
        self.forest[u].append((v, w))
        self.forest[v].append((u, w))
        edge_key = (min(u, v), max(u, v), w)
        self.mst_edges.add(edge_key)

    def _remove_edge(self, u, v, w):
        self.forest[u] = [(nbr, wt) for nbr, wt in self.forest[u] if not (nbr == v and wt == w)]
        self.forest[v] = [(nbr, wt) for nbr, wt in self.forest[v] if not (nbr == u and wt == w)]
        edge_key = (min(u, v), max(u, v), w)
        if edge_key in self.mst_edges:
            self.mst_edges.remove(edge_key)

    def is_connected(self, start, goal):
        visited = set()
        deq = deque([start])
        while deq:
            for _ in range(len(deq)):
                cur_vertex = deq.popleft()
                if cur_vertex == goal:
                    return True
                if cur_vertex in visited:
                    continue
                visited.add(cur_vertex)
                for neighbor, _ in self.forest.get(cur_vertex, []):
                    if neighbor not in visited:
                        deq.append(neighbor)

    def find_path(self, start, goal, visited=None):
        if visited is None:
            visited = set()
            
        if start == goal:
            return []
        
        visited.add(start)
        
        for neighbor, c in self.forest[start]:
            if neighbor in visited:
                continue
            subpath = self.find_path(neighbor, goal, visited)
            if subpath is not None:
                return [(start, neighbor, c)] + subpath
        return None

    def get_mst_edges(self):
        return self.mst_edges
