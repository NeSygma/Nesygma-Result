from z3 import *

# Boolean variable for each vertex 1..24
selected = [Bool(f'sel_{i}') for i in range(1, 25)]

# Edge list
edges = [
    (1,2),(1,4),(1,10),(1,17),
    (2,5),(2,9),
    (3,6),
    (4,7),(5,8),(6,7),
    (8,16),(8,24),
    (9,10),(9,12),(9,17),
    (10,14),
    (11,15),
    (12,16),
    (13,14),
    (16,24),
    (17,18),(17,20),
    (18,19),(18,21),
    (19,22),
    (20,23),
    (21,24)
]

solver = Optimize()

# Independence constraints: no edge can have both endpoints selected
for (u,v) in edges:
    solver.add(Not(And(selected[u-1], selected[v-1])))

# Core vertices: 1,9,17
core_vertices = [1,9,17]
core_count = Sum([selected[c-1] for c in core_vertices])
solver.add(core_count <= 2)

# Core-support dependency
# zone 1 support: 2,3
# zone 2 support: 10,11
# zone 3 support: 18,19
solver.add(Implies(selected[0], Or(selected[1], selected[2])))  # core 1 -> support 2 or 3
solver.add(Implies(selected[8], Or(selected[9], selected[10]))) # core 9 -> support 10 or 11
solver.add(Implies(selected[16], Or(selected[17], selected[18]))) # core 17 -> support 18 or 19

# Conditional zone exclusion
# peripheral vertices in zone 1: 4,5,6,7,8
peripheral_zone1 = [4,5,6,7,8]
# all vertices in zone 3: 17-24
zone3_vertices = list(range(17,25))
p1 = Or([selected[v-1] for v in peripheral_zone1])
z3 = Or([selected[v-1] for v in zone3_vertices])
solver.add(Implies(p1, Not(z3)))

# Peripheral headcount rule
peripheral_vertices = [4,5,6,7,8,12,13,14,15,16,20,21,22,23,24]
peripheral_count = Sum([selected[v-1] for v in peripheral_vertices])
solver.add(peripheral_count <= core_count)

# Objective: maximize total size
size = Sum([selected[i-1] for i in range(1,25)])
solver.maximize(size)

# Solve
result = solver.check()
if result == sat:
    print("STATUS: sat")
    m = solver.model()
    # Build result lists
    independent_set = [i+1 for i in range(24) if is_true(m[selected[i]])]
    core_set = [c for c in core_vertices if is_true(m[selected[c-1]])]
    support_set = [s for s in [2,3,10,11,18,19] if is_true(m[selected[s-1]])]
    peripheral_set = [p for p in peripheral_vertices if is_true(m[selected[p-1]])]
    core_cnt = len(core_set)
    support_cnt = len(support_set)
    peripheral_cnt = len(peripheral_set)
    print("independent_set:", independent_set)
    print("size:", len(independent_set))
    print("core_vertices:", core_set)
    print("support_vertices:", support_set)
    print("peripheral_vertices:", peripheral_set)
    print("core_count:", core_cnt)
    print("support_count:", support_cnt)
    print("peripheral_count:", peripheral_cnt)
else:
    print("STATUS: unsat")