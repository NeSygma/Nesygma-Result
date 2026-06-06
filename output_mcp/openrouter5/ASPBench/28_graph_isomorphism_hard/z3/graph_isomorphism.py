from z3 import *

# Create solver
solver = Solver()

# G1 vertices: 1,2,3,4,5,6,7,8
# G2 vertices: a,b,c,d,e,f,g,h (we'll encode as 0..7)
g1_vertices = [1, 2, 3, 4, 5, 6, 7, 8]
g2_vertices = [0, 1, 2, 3, 4, 5, 6, 7]  # a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7

# Map G2 vertex names to indices
g2_names = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

# Colors: Red=0, Blue=1
# G1 colors: Red: 1,2,5,6; Blue: 3,4,7,8
g1_colors = {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1}
# G2 colors: Red: a,b,e,f (0,1,4,5); Blue: c,d,g,h (2,3,6,7)
g2_colors = {0: 0, 1: 0, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1}

# Special vertices: G1: {1}, G2: {a=0}
g1_special = {1}
g2_special = {0}

# Edges for G1: (u,v,w) - undirected
g1_edges = [
    (1,3,10), (1,4,20), (2,3,20), (2,4,10),
    (5,7,10), (5,8,20), (6,7,20), (6,8,10),
    (1,5,30), (2,6,30), (3,7,40), (4,8,40)
]

# Edges for G2: (u,v,w) - undirected, using indices
g2_edges = [
    (0,2,10), (0,3,20), (1,2,20), (1,3,10),
    (4,6,10), (4,7,20), (5,6,20), (5,7,10),
    (0,4,30), (1,5,30), (2,6,40), (3,7,40)
]

# Build adjacency sets for quick lookup
g1_adj = {}
for u,v,w in g1_edges:
    g1_adj.setdefault((u,v), w)
    g1_adj.setdefault((v,u), w)

g2_adj = {}
for u,v,w in g2_edges:
    g2_adj.setdefault((u,v), w)
    g2_adj.setdefault((v,u), w)

# Decision variables: f[i] = G2 vertex index that G1 vertex i maps to
f = [Int(f'f_{i}') for i in range(1, 9)]  # index by G1 vertex number

# Domain: each f[i] is in {0..7}
for i in range(1, 9):
    solver.add(f[i-1] >= 0, f[i-1] <= 7)

# Constraint 1: Bijection - one-to-one and onto
solver.add(Distinct(f))

# Constraint 2: Color preservation
for v in range(1, 9):
    # f(v) must have same color as v
    # Use Or-loop to constrain
    same_color_conds = []
    for g2v in range(8):
        if g1_colors[v] == g2_colors[g2v]:
            same_color_conds.append(f[v-1] == g2v)
    solver.add(Or(same_color_conds))

# Constraint 3: Special vertex preservation
# Vertex 1 is special in G1, must map to special vertex in G2 (which is a=0)
solver.add(f[0] == 0)  # 1 -> a

# Constraint 4: Edge and weight preservation
# For every pair of G1 vertices (u,v), check if edge exists in G1
# If edge (u,v,w) in G1, then (f(u), f(v), w) must be in G2
# If no edge in G1, then (f(u), f(v)) must not be an edge in G2

for u in range(1, 9):
    for v in range(u+1, 9):
        edge_key = (u,v) if (u,v) in g1_adj else (v,u)
        if edge_key in g1_adj:
            w = g1_adj[edge_key]
            # Edge exists in G1 with weight w
            # So (f(u), f(v), w) must exist in G2
            edge_conds = []
            for (g2u, g2v, g2w) in g2_edges:
                edge_conds.append(And(f[u-1] == g2u, f[v-1] == g2v, w == g2w))
                edge_conds.append(And(f[u-1] == g2v, f[v-1] == g2u, w == g2w))
            solver.add(Or(edge_conds))
        else:
            # No edge in G1
            # So (f(u), f(v)) must not be an edge in G2
            no_edge_conds = []
            for (g2u, g2v, _) in g2_edges:
                no_edge_conds.append(Not(And(f[u-1] == g2u, f[v-1] == g2v)))
                no_edge_conds.append(Not(And(f[u-1] == g2v, f[v-1] == g2u)))
            solver.add(And(no_edge_conds))

# Constraint 5: Forbidden subgraph - no 3-cycle involving special vertex (a=0) with total weight exactly 60
# Special vertex in G2 is a=0, which is f[0] (mapping of G1 vertex 1)
# We need to check all triples (0, x, y) where x,y are distinct G2 vertices
# If (0,x), (0,y), (x,y) are all edges, and weights sum to 60, it's forbidden

# Build G2 edge weight lookup
g2_edge_weights = {}
for u,v,w in g2_edges:
    g2_edge_weights[(u,v)] = w
    g2_edge_weights[(v,u)] = w

# For each pair of G2 vertices (x,y) distinct from 0
for x in range(1, 8):
    for y in range(x+1, 8):
        # Check if triangle (0,x,y) exists in G2
        if (0,x) in g2_edge_weights and (0,y) in g2_edge_weights and (x,y) in g2_edge_weights:
            total_w = g2_edge_weights[(0,x)] + g2_edge_weights[(0,y)] + g2_edge_weights[(x,y)]
            if total_w == 60:
                # This triangle is forbidden. The mapping must not map any G1 vertices to x and y
                # such that the corresponding G1 vertices also form a triangle with vertex 1
                # Actually, the constraint says: the mapping is invalid if it CREATES a 3-cycle in G2
                # that involves a special vertex and has total weight exactly 60.
                # Since the special vertex is fixed at a=0, and the edges/weights are preserved,
                # this means we must avoid mapping G1 vertices to x,y such that the pre-images
                # in G1 form a triangle with vertex 1 with total weight 60.
                
                # Find which G1 vertices could map to x and y
                # The forbidden condition is: there exist G1 vertices u,v such that
                # f(u)=x, f(v)=y, and (1,u,w1), (1,v,w2), (u,v,w3) are edges in G1 with w1+w2+w3=60
                
                # Check all pairs of G1 vertices (u,v) distinct from 1
                for u in range(2, 9):
                    for v in range(u+1, 9):
                        # Check if (1,u), (1,v), (u,v) are edges in G1
                        e1u = (1,u) if (1,u) in g1_adj else (u,1) if (u,1) in g1_adj else None
                        e1v = (1,v) if (1,v) in g1_adj else (v,1) if (v,1) in g1_adj else None
                        euv = (u,v) if (u,v) in g1_adj else (v,u) if (v,u) in g1_adj else None
                        
                        if e1u and e1v and euv:
                            w1 = g1_adj[e1u]
                            w2 = g1_adj[e1v]
                            w3 = g1_adj[euv]
                            if w1 + w2 + w3 == 60:
                                # This would create a forbidden triangle
                                solver.add(Not(And(f[u-1] == x, f[v-1] == y)))
                                solver.add(Not(And(f[u-1] == y, f[v-1] == x)))

# Check
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    print("is_isomorphic: true")
    
    # Build mapping
    mapping = {}
    for i in range(1, 9):
        g2_idx = m.eval(f[i-1]).as_long()
        mapping[str(i)] = g2_names[g2_idx]
    
    print("mapping:", mapping)
    
    # Build preserved weighted edges
    preserved_edges = []
    for (u,v,w) in g1_edges:
        g2_u = m.eval(f[u-1]).as_long()
        g2_v = m.eval(f[v-1]).as_long()
        g1_edge = sorted([str(u), str(v)])
        g2_edge = sorted([g2_names[g2_u], g2_names[g2_v]])
        preserved_edges.append([[g1_edge[0], g1_edge[1], w], [g2_edge[0], g2_edge[1], w]])
    
    print("preserved_weighted_edges:", preserved_edges)
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")