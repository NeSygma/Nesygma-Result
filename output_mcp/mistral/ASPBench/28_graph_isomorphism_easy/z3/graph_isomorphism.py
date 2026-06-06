from z3 import *

# Define the vertices for G1 and G2
# G1 vertices: 0, 1, 2, 3, 4
# G2 vertices: a, b, c, d, e (mapped to 0, 1, 2, 3, 4 for Z3 simplicity)
G1_vertices = [0, 1, 2, 3, 4]
G2_vertices = [0, 1, 2, 3, 4]  # a=0, b=1, c=2, d=3, e=4

# Define edges for G1 and G2
# G1 edges: (0,1), (0,2), (1,3), (2,4), (3,4)
G1_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]

# G2 edges: (a,b), (a,c), (b,d), (c,e), (d,e) -> (0,1), (0,2), (1,3), (2,4), (3,4)
G2_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]

# Compute degrees for G1 and G2
def compute_degrees(vertices, edges):
    degree = {v: 0 for v in vertices}
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    return degree

G1_degree = compute_degrees(G1_vertices, G1_edges)
G2_degree = compute_degrees(G2_vertices, G2_edges)

# Create a solver
solver = Solver()

# Define the mapping function f: G1_vertices -> G2_vertices
f = Function('f', IntSort(), IntSort())

# Ensure f is a bijection (permutation)
# We can model this by ensuring f is injective and surjective over the finite domain
# For finite domains, injective + same cardinality implies bijective
# We'll enforce that f is injective and that the image of f is exactly G2_vertices

# Injectivity: f(u) != f(v) for u != v
for u in G1_vertices:
    for v in G1_vertices:
        if u != v:
            solver.add(f(u) != f(v))

# Surjectivity: Every vertex in G2 is mapped to by some vertex in G1
# We can enforce that the set {f(u) | u in G1_vertices} = G2_vertices
# This is equivalent to saying that for every y in G2_vertices, there exists x in G1_vertices such that f(x) = y
# We can encode this by ensuring that the image of f covers all G2_vertices
for y in G2_vertices:
    solver.add(Or([f(x) == y for x in G1_vertices]))

# Adjacency preservation: For every edge (u,v) in G1, (f(u), f(v)) must be in G2
for u, v in G1_edges:
    solver.add(Or([And(f(u) == x, f(v) == y) for (x, y) in G2_edges]))

# Reverse adjacency preservation: For every edge (x,y) in G2, (f^{-1}(x), f^{-1}(y)) must be in G1
# Since f is a bijection, we can compute the inverse mapping implicitly
# For each edge (x,y) in G2, there must exist u, v in G1 such that f(u)=x, f(v)=y, and (u,v) in G1_edges
for x, y in G2_edges:
    solver.add(Or([And(f(u) == x, f(v) == y, Or([And(u == uu, v == vv) for (uu, vv) in G1_edges])) for u in G1_vertices for v in G1_vertices]))

# Degree preservation: For every u in G1, degree(u) = degree(f(u))
# We need to ensure that for each u in G1, the degree of u in G1 equals the degree of the vertex in G2 that u maps to
for u in G1_vertices:
    for y in G2_vertices:
        solver.add(Implies(f(u) == y, G1_degree[u] == G2_degree[y]))

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    # Extract the mapping
    mapping = {u: model.eval(f(u)) for u in G1_vertices}
    # Convert G2 vertex indices back to letters for output
    vertex_to_letter = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}
    mapping_str = {u: vertex_to_letter[model.eval(f(u)).as_long()] for u in G1_vertices}
    
    # Extract preserved edges
    preserved_edges = []
    for u, v in G1_edges:
        fu = model.eval(f(u)).as_long()
        fv = model.eval(f(v)).as_long()
        preserved_edges.append([f"{u},{v}", f"{vertex_to_letter[fu]},{vertex_to_letter[fv]}"])
    
    print("STATUS: sat")
    print("is_isomorphic = True")
    print("mapping =", mapping_str)
    print("preserved_edges =", preserved_edges)
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")