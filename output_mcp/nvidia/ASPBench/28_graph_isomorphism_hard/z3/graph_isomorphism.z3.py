from z3 import *
from collections import defaultdict

solver = Solver()

# Mapping variables
mapping = [Int(f'm{i}') for i in range(1,9)]

# Domain constraints
for m in mapping:
    solver.add(m >= 0, m <= 7)

# AllDifferent
solver.add(Distinct(mapping))

# Special vertex: vertex 1 maps to a (index 0)
solver.add(mapping[0] == 0)

# Color constraints
red_indices = [0,1,4,5]  # a,b,e,f
blue_indices = [2,3,6,7]  # c,d,g,h
red_vertices = [1,2,5,6]  # G1 red vertices
blue_vertices = [3,4,7,8]  # G1 blue vertices

for v in red_vertices:
    idx = v-1
    solver.add(Or([mapping[idx] == r for r in red_indices]))

for v in blue_vertices:
    idx = v-1
    solver.add(Or([mapping[idx] == b for b in blue_indices]))

# Edge preservation
g2_edges = [
    (0,2,10), (0,3,20), (1,2,20), (1,3,10),
    (4,6,10), (4,7,20), (5,6,20), (5,7,10),
    (0,4,30), (1,5,30), (2,6,40), (3,7,40)
]

g1_edges = [
    (1,3,10), (1,4,20), (2,3,20), (2,4,10),
    (5,7,10), (5,8,20), (6,7,20), (6,8,10),
    (1,5,30), (2,6,30), (3,7,40), (4,8,40)
]

# Map weight to pairs
weight_to_pairs = defaultdict(list)
for i,j,w in g2_edges:
    weight_to_pairs[w].append((i,j))

# Add constraints for each G1 edge
for (u,v,w) in g1_edges:
    pairs = weight_to_pairs[w]
    or_terms = []
    for (i,j) in pairs:
        term1 = And(mapping[u-1] == i, mapping[v-1] == j)
        term2 = And(mapping[u-1] == j, mapping[v-1] == i)
        or_terms.append(term1)
        or_terms.append(term2)
    solver.add(Or(*or_terms))

# Check solution
result = solver.check()
BENCHMARK_MODE = True

if result == sat:
    print('STATUS: sat')
    model = solver.model()
    g2_names = ['a','b','c','d','e','f','g','h']
    mapping_dict = {}
    for i, var in enumerate(mapping, start=1):
        idx = model.eval(var).as_long()
        mapping_dict[str(i)] = g2_names[idx]
    # Print mapping
    print('mapping: ' + ', '.join([f'{k}->{v}' for k,v in mapping_dict.items()]))
    # Print preserved_weighted_edges
    edge_strs = []
    for (u,v,w) in g1_edges:
        u_img = mapping_dict[str(u)]
        v_img = mapping_dict[str(v)]
        edge_strs.append(f'{u}-{v}->{u_img}-{v_img}')
    print('preserved_weighted_edges: ' + ', '.join(edge_strs))
elif result == unsat:
    print('STATUS: unsat')
    if BENCHMARK_MODE:
        print('RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)')
else:
    print('STATUS: unknown')