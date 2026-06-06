from z3 import *

solver = Optimize()

# Variables: part1[v] indicates vertex v is in partition 1
part1 = [Bool(f'p1_{i}') for i in range(8)]

# Exactly 4 vertices in partition 1
solver.add(Sum([If(part1[i], 1, 0) for i in range(8)]) == 4)

# List of edges
edges = [(0,1),(0,4),(1,2),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7)]

# Crossing variables: XOR of partition assignment
crossings = []
for (u,v) in edges:
    cross = If(And(part1[u], Not(part1[v])) | And(Not(part1[u]), part1[v]), 1, 0)
    crossings.append(cross)

# Cut size as sum of crossing variables
cut_size = Sum(crossings)

# Objective: minimize cut size
solver.minimize(cut_size)

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    # Extract partition sets
    part1_set = [i for i in range(8) if model.eval(part1[i])]
    part2_set = [i for i in range(8) if not model.eval(part1[i])]
    # Compute cut edges
    cut_edges = []
    for (u,v) in edges:
        if model.eval(crossings[edges.index((u,v))]):
            if u < v:
                cut_edges.append({'from': u, 'to': v})
            else:
                cut_edges.append({'from': v, 'to': u})
    # Print results
    print("STATUS: sat")
    print("partition_1:", part1_set)
    print("partition_2:", part2_set)
    print("cut_size:", sum(model.eval(c) for c in crossings))
    print("cut_edges:", cut_edges)
    print("balance: sizes=[4,4], status=balanced")
else:
    print("STATUS: unsat")