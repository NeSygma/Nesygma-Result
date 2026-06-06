from z3 import *

# Define vertices and edges
vertices = list(range(8))
edges = [(0,1), (0,4), (1,2), (1,5), (2,3), (2,6), (3,7), (4,5), (4,6), (5,7), (6,7)]

# Bool variable: True means in partition 1, False means partition 2
in_part1 = [Bool(f"p1_{v}") for v in vertices]

opt = Optimize()
# Exactly 4 vertices in partition 1
opt.add(Sum([If(b, 1, 0) for b in in_part1]) == 4)
# No need for explicit partition 2 count; total vertices = 8

# Define cut size (edges crossing partitions)
cross_terms = []
for (u, v) in edges:
    cross_terms.append(If(in_part1[u] != in_part1[v], 1, 0))
cut_size = Sum(cross_terms)
opt.minimize(cut_size)

res = opt.check()
if res == sat:
    m = opt.model()
    # Build partitions based on model values
    part1 = [v for v in vertices if is_true(m.eval(in_part1[v]))]
    part2 = [v for v in vertices if not is_true(m.eval(in_part1[v]))]
    # Determine crossing edges using concrete boolean evaluation
    cut_edges = []
    for (u, v) in edges:
        if is_true(m.eval(in_part1[u])) != is_true(m.eval(in_part1[v])):
            a, b = (u, v) if u < v else (v, u)
            cut_edges.append((a, b))
    cut_sz = len(cut_edges)
    balance = {"partition1_size": len(part1), "partition2_size": len(part2), "status": "balanced" if len(part1)==len(part2)==4 else "unbalanced"}
    print("STATUS: sat")
    print("partition_1 =", part1)
    print("partition_2 =", part2)
    print("cut_size =", cut_sz)
    print("cut_edges =", cut_edges)
    print("balance =", balance)
else:
    print("STATUS: unsat" if res == unsat else "STATUS: unknown")