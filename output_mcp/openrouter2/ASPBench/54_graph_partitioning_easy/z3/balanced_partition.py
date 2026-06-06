from z3 import *

# Problem data
vertices = list(range(8))
edges = [(0,1),(0,4),(1,2),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7)]

# Solver
opt = Optimize()

# Partition variables: 0 or 1
part = [Int(f'part_{i}') for i in vertices]
for p in part:
    opt.add(p >= 0, p <= 1)

# Exactly 4 vertices in partition 1 (value 1)
opt.add(Sum(part) == 4)

# Cut size variable
cut_size = Int('cut_size')
# Define cut edges as boolean expressions
cut_edge_bools = []
for (u,v) in edges:
    # cut if partitions differ
    cut_edge_bools.append(part[u] != part[v])
# cut_size = sum of cut edges
opt.add(cut_size == Sum([If(b, 1, 0) for b in cut_edge_bools]))

# Objective: minimize cut size
opt.minimize(cut_size)

# Solve
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract partitions
    partition1 = [i for i in vertices if model[part[i]].as_long() == 1]
    partition2 = [i for i in vertices if model[part[i]].as_long() == 0]
    # Extract cut edges
    cut_edges = []
    for (u,v) in edges:
        if model[part[u]].as_long() != model[part[v]].as_long():
            cut_edges.append({'from': min(u,v), 'to': max(u,v)})
    # Cut size
    cs = model[cut_size].as_long()
    # Balance info
    balance = {
        'size1': len(partition1),
        'size2': len(partition2),
        'balanced': len(partition1) == len(partition2)
    }
    # Output
    print("STATUS: sat")
    print("partition_1:", partition1)
    print("partition_2:", partition2)
    print("cut_size:", cs)
    print("cut_edges:", cut_edges)
    print("balance:", balance)
else:
    print("STATUS: unsat")
    if result == unknown:
        print("STATUS: unknown")