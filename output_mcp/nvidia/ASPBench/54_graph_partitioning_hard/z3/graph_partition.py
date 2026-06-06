from z3 import *

part = [Int(f'p{i}') for i in range(16)]

opt = Optimize()

# domain 0..3
for i in range(16):
    opt.add(part[i] >= 0, part[i] <= 3)

# exactly 4 per partition
for p in range(4):
    opt.add(Sum([If(part[i] == p, 1, 0) for i in range(16)]) == 4)

edges = [
    (0,1,10),(0,2,10),(0,3,10),
    (1,2,10),(1,3,10),(2,3,10),
    (4,5,10),(4,6,10),(4,7,10),
    (5,6,10),(5,7,10),(6,7,10),
    (8,9,10),(8,10,10),(8,11,10),
    (9,10,10),(9,11,10),(10,11,10),
    (12,13,10),(12,14,10),(12,15,10),
    (13,14,10),(13,15,10),(14,15,10),
    (3,4,1),(7,8,2),(11,12,3),(15,0,1),
    (1,6,2),(5,10,3),(9,14,1)
]

# objective
obj = Sum([w * If(part[u] != part[v], 1, 0) for (u,v,w) in edges])
opt.minimize(obj)

result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    cut_weight = model.eval(obj)
    print("cut_weight:", cut_weight)
    cut_edges = []
    for (u,v,w) in edges:
        if model.eval(If(part[u] != part[v], 1, 0)) == 1:
            cut_edges.append((u,v))
    print("cut_edges:", cut_edges)
    # gather partitions
    partitions = {p: [] for p in range(4)}
    for i in range(16):
        p_val = model.eval(part[i]).as_long()  # convert to Python int
        partitions[p_val].append(i)
    for p in range(4):
        print(f"partition_{p+1}: {partitions[p]}")
    print("balance: each partition has 4 vertices")
else:
    print("STATUS: unsat")