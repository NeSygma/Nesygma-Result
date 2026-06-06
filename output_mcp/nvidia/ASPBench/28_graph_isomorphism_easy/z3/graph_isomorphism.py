from z3 import *

solver = Solver()

# Mapping variables: f_i is the image of G1 vertex i in G2 (0..4)
f = [Int(f'f_{i}') for i in range(5)]

# Domain constraints
for i in range(5):
    solver.add(f[i] >= 0, f[i] < 5)

# All-different (bijection)
solver.add(Distinct(f))

# Graph edges (undirected)
g1_edges = [(0,1),(0,2),(1,3),(2,4),(3,4)]
g2_edges = [(0,1),(0,2),(1,3),(2,4),(3,4)]

# Forward adjacency preservation: each G1 edge maps to a G2 edge
for (u,v) in g1_edges:
    choices = []
    for (x,y) in g2_edges:
        choices.append(And(f[u]==x, f[v]==y))
        choices.append(And(f[u]==y, f[v]==x))
    solver.add(Or(choices))

# Reverse adjacency preservation: each G2 edge must be hit by some G1 edge
for (x,y) in g2_edges:
    choices = []
    for (u,v) in g1_edges:
        choices.append(And(f[u]==x, f[v]==y))
        choices.append(And(f[u]==y, f[v]==x))
    solver.add(Or(choices))

# Check satisfiability
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    model = solver.model()
    # Map indices to letters a-e
    letter_map = {0:'a',1:'b',2:'c',3:'d',4:'e'}
    # Build mapping dictionary (G1 vertex -> G2 vertex letter)
    mapping_dict = {str(i): letter_map[model.eval(f[i], model_completion=True).as_long()] for i in range(5)}
    # Build preserved_edges list
    preserved_edges = []
    for (u,v) in g1_edges:
        fu = model.eval(f[u], model_completion=True).as_long()
        fv = model.eval(f[v], model_completion=True).as_long()
        src = f"{u},{v}"
        dst = f"{letter_map[fu]},{letter_map[fv]}"
        preserved_edges.append([src, dst])
    # Output results
    print("STATUS: sat")
    print(f"is_isomorphic = True")
    print(f"mapping = {mapping_dict}")
    print(f"preserved_edges = {preserved_edges}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")