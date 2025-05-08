from toptree import Vertex

def parse_dimacs_maxflow(filename):
    edges = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('c') or line == "":  
                continue
            
            parts = line.split()
            if parts[0] == 'p':
                num_vertices = int(parts[2]) 
                vertices = [Vertex(i) for i in range(num_vertices+1)]
            if parts[0] == 'a':
                u, v, capacity = int(parts[1]), int(parts[2]), int(parts[3])
                edges.append((vertices[u], vertices[v], capacity))
            elif parts[0] == 'n':
                if parts[2] == 's':
                    s = vertices[int(parts[1])]
                elif parts[2] == 't':
                    t = vertices[int(parts[1])]
    return edges