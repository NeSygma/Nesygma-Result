from z3 import *

# Problem data
vertices = [1,2,3,4,5,6]
edges = [(1,2),(1,3),(2,4),(2,5),(3,4),(3,6),(4,2),(4,5),(5,3),(5,6),(6,1),(6,4)]

# Solver
opt = Optimize()

# Decision variables
removed = {v: Bool(f"removed_{v}") for v in vertices}
order = {v: Int(f"order_{v}") for v in vertices}

# Domain constraints for order
n = len(vertices)
for v in vertices:
    opt.add(order[v] >= 0, order[v] < n)

# Acyclicity constraints: for each edge u->v, if both vertices remain, order[u] < order[v]
for (u,v) in edges:
    opt.add(Implies(And(Not(removed[u]), Not(removed[v])), order[u] < order[v]))

# Objective: minimize number of removed vertices
obj = Sum([If(removed[v], 1, 0) for v in vertices])
opt.minimize(obj)

# Solve
result = opt.check()
if result == sat:
    m = opt.model()
    removed_vertices = [v for v in vertices if is_true(m[removed[v]])]
    print("STATUS: sat")
    print("removed_vertices =", removed_vertices)
    print("size =", len(removed_vertices))
else:
    print("STATUS: unsat")