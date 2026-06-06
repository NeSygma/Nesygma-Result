from z3 import *

# Define vertices 0..15
n = 16
vs = [Bool(f'v{i}') for i in range(n)]

# Costs
costs = [1]*n
for i in [2,10,14]:
    costs[i] = 3

solver = Optimize()
# Standard edges constraints
standard_edges = [(1,3),(1,4),(2,6),(3,7),(4,8),(5,11),(6,7),(7,12),(8,12),(11,13),(12,13),(13,14)]
for u,v in standard_edges:
    solver.add(Or(vs[u], vs[v]))
# Heavy edges constraints
# (0,5) master 0, (9,10) none, (14,15) master 15
# General rule: both endpoints must be selected unless master present, then master alone suffices.
# Implement as described: for (0,5) require v0, for (14,15) require v15, for (9,10) require both.
solver.add(vs[0])  # heavy edge (0,5) covered by master 0
solver.add(vs[15]) # heavy edge (14,15) covered by master 15
solver.add(And(vs[9], vs[10])) # heavy edge (9,10) both needed
# Antagonistic pairs: at most one
antagonistic = [(1,2),(8,9)]
for u,v in antagonistic:
    solver.add(Not(And(vs[u], vs[v])))
# Objective: minimize total cost
total_cost = Sum([If(vs[i], costs[i], 0) for i in range(n)])
solver.minimize(total_cost)

if solver.check() == sat:
    m = solver.model()
    selected = [i for i in range(n) if m.eval(vs[i])]
    total = sum(costs[i] for i in selected)
    print("STATUS: sat")
    print("selected_vertices =", selected)
    print("total_cost =", total)
else:
    print("STATUS: unsat")