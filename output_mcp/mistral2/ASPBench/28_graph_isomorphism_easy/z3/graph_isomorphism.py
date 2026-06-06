from z3 import *

# Define the vertices for G1 and G2
G1_vertices = [0, 1, 2, 3, 4]
G2_vertices = ['a', 'b', 'c', 'd', 'e']

# Map G2 vertices to integers for easier indexing
G2_vertex_to_int = {v: i for i, v in enumerate(G2_vertices)}
G2_int_to_vertex = {i: v for i, v in enumerate(G2_vertices)}

# Define edges for G1 and G2
G1_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]
G2_edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]

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

# Declare the mapping from G1 vertices to G2 vertices (as integers)
mapping = [Int(f'mapping_{i}') for i in G1_vertices]

# Constraint 1: Bijection (injective and surjective)
# Injective: All mapped values are distinct
solver.add(Distinct(mapping))

# Constraint 2: Adjacency preservation
for u, v in G1_edges:
    # For edge (u,v) in G1, (mapping[u], mapping[v]) must be an edge in G2
    # We need to check if (mapping[u], mapping[v]) is in G2_edges
    # Since G2_edges are tuples of strings, we need to convert the mapped integers back to strings
    solver.add(
        Or(
            And(
                mapping[u] == G2_vertex_to_int['a'],
                mapping[v] == G2_vertex_to_int['b']
            ),
            And(
                mapping[u] == G2_vertex_to_int['a'],
                mapping[v] == G2_vertex_to_int['c']
            ),
            And(
                mapping[u] == G2_vertex_to_int['b'],
                mapping[v] == G2_vertex_to_int['d']
            ),
            And(
                mapping[u] == G2_vertex_to_int['c'],
                mapping[v] == G2_vertex_to_int['e']
            ),
            And(
                mapping[u] == G2_vertex_to_int['d'],
                mapping[v] == G2_vertex_to_int['e']
            ),
            And(
                mapping[u] == G2_vertex_to_int['b'],
                mapping[v] == G2_vertex_to_int['a']
            ),
            And(
                mapping[u] == G2_vertex_to_int['c'],
                mapping[v] == G2_vertex_to_int['a']
            ),
            And(
                mapping[u] == G2_vertex_to_int['d'],
                mapping[v] == G2_vertex_to_int['b']
            ),
            And(
                mapping[u] == G2_vertex_to_int['e'],
                mapping[v] == G2_vertex_to_int['c']
            ),
            And(
                mapping[u] == G2_vertex_to_int['e'],
                mapping[v] == G2_vertex_to_int['d']
            )
        )
    )

# Constraint 3: Reverse adjacency preservation
# For every edge (x,y) in G2, (f⁻¹(x), f⁻¹(y)) must be an edge in G1
# To implement this, we need to ensure that for every edge (x,y) in G2,
# there exists a pair (u,v) in G1 such that mapping[u] = x and mapping[v] = y
for x, y in G2_edges:
    # Check if there exists u, v in G1 such that mapping[u] = G2_vertex_to_int[x] and mapping[v] = G2_vertex_to_int[y]
    # and (u,v) is an edge in G1
    solver.add(
        Or(
            And(
                mapping[0] == G2_vertex_to_int[x],
                mapping[1] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[0] == G2_vertex_to_int[x],
                mapping[2] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[0] == G2_vertex_to_int[x],
                mapping[3] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[0] == G2_vertex_to_int[x],
                mapping[4] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[1] == G2_vertex_to_int[x],
                mapping[2] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[1] == G2_vertex_to_int[x],
                mapping[3] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[1] == G2_vertex_to_int[x],
                mapping[4] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[2] == G2_vertex_to_int[x],
                mapping[3] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[2] == G2_vertex_to_int[x],
                mapping[4] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            ),
            And(
                mapping[3] == G2_vertex_to_int[x],
                mapping[4] == G2_vertex_to_int[y],
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            )
        )
    )

# Constraint 4: Degree preservation
for u in G1_vertices:
    solver.add(
        Or(
            And(
                mapping[u] == G2_vertex_to_int['a'],
                G1_degree[u] == G2_degree['a']
            ),
            And(
                mapping[u] == G2_vertex_to_int['b'],
                G1_degree[u] == G2_degree['b']
            ),
            And(
                mapping[u] == G2_vertex_to_int['c'],
                G1_degree[u] == G2_degree['c']
            ),
            And(
                mapping[u] == G2_vertex_to_int['d'],
                G1_degree[u] == G2_degree['d']
            ),
            And(
                mapping[u] == G2_vertex_to_int['e'],
                G1_degree[u] == G2_degree['e']
            )
        )
    )

# Check if the graphs are isomorphic
result = solver.check()

if result == sat:
    model = solver.model()
    # Extract the mapping
    mapping_dict = {}
    for u in G1_vertices:
        mapped_val = model[mapping[u]]
        # Convert the integer back to the G2 vertex
        for v, i in G2_vertex_to_int.items():
            if i == mapped_val:
                mapping_dict[u] = v
                break

    # Extract preserved edges
    preserved_edges = []
    for u, v in G1_edges:
        mapped_u = mapping_dict[u]
        mapped_v = mapping_dict[v]
        preserved_edges.append([f"{u},{v}", f"{mapped_u},{mapped_v}"])

    print("STATUS: sat")
    print("is_isomorphic = True")
    print("mapping =", mapping_dict)
    print("preserved_edges =", preserved_edges)
elif result == unsat:
    print("STATUS: unsat")
    print("is_isomorphic = False")
    print("mapping = null")
    print("preserved_edges = []")
else:
    print("STATUS: unknown")