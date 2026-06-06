from z3 import *

# Create optimizer
opt = Optimize()

# Vertices 1..6
colors = [Int(f'c{i}') for i in range(1,7)]

# Number of colors variable
K = Int('K')

# Each vertex gets a color in [1, K]
for i, var in enumerate(colors, start=1):
    opt.add(var >= 1, var <= K)

# Edge list
edges = [(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,5),(4,6),(5,6)]

# Adjacent vertices must differ
for u,v in edges:
    opt.add(colors[u-1] != colors[v-1])

# Objective: minimize K (the number of colors)
opt.minimize(K)

# Solve
result = opt.check()
if result == sat:
    print("STATUS: sat")
    m = opt.model()
    K_val = m[K].as_long()
    print(f"num_colors = {K_val}")
    for i in range(1,7):
        print(f"color[{i}] = {m[colors[i-1]].as_long()}")
else:
    print("STATUS: unsat")