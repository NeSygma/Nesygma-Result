from z3 import *

# Vertices: 0..7
N = 8
vertices = list(range(N))

# Edges
edges = [(0,1), (0,4),
         (1,2), (1,5),
         (2,3), (2,6),
         (3,7),
         (4,5), (4,6),
         (5,7),
         (6,7)]

# Decision variables: part[v] = 0 or 1 (partition assignment)
part = [Int(f'part_{v}') for v in vertices]

opt = Optimize()

# Domain: each vertex in {0, 1}
for v in vertices:
    opt.add(Or(part[v] == 0, part[v] == 1))

# Exactly 4 vertices in partition 0 (and thus 4 in partition 1)
opt.add(Sum([If(part[v] == 0, 1, 0) for v in vertices]) == 4)

# Objective: minimize cut size
# An edge (u,v) crosses if part[u] != part[v]
cut_size = Sum([If(part[u] != part[v], 1, 0) for (u, v) in edges])
opt.minimize(cut_size)

# Solve
result = opt.check()

if result == sat:
    m = opt.model()
    p0 = [v for v in vertices if m.eval(part[v]).as_long() == 0]
    p1 = [v for v in vertices if m.eval(part[v]).as_long() == 1]
    cut_edges_list = []
    for (u, v) in edges:
        if m.eval(part[u]).as_long() != m.eval(part[v]).as_long():
            cut_edges_list.append((u, v))
    print("STATUS: sat")
    print(f"partition_1 = {p0}")
    print(f"partition_2 = {p1}")
    print(f"cut_size = {len(cut_edges_list)}")
    print(f"cut_edges = {cut_edges_list}")
    print(f"balance = {{'size1': {len(p0)}, 'size2': {len(p1)}, 'balanced': {len(p0) == len(p1)}}}")
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")