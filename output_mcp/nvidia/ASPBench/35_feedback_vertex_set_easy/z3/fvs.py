from z3 import *

# Boolean variable for each vertex: True if removed
remove = [Bool(f'remove_{i}') for i in range(1, 7)]
# Integer order variable for each vertex (used to enforce acyclicity on kept vertices)
order = [Int(f'order_{i}') for i in range(1, 7)]

# Constrain order variables to a small range to keep them bounded
for o in order:
    o >= 0
    o <= 5

# Define the directed edges of the graph
edges = [
    (1, 2), (1, 3),
    (2, 4), (2, 5),
    (3, 4), (3, 6),
    (4, 2), (4, 5),
    (5, 3), (5, 6),
    (6, 1), (6, 4)
]

# Create an Optimize instance for minimization
solver = Optimize()

# Objective: minimize the number of removed vertices
solver.minimize(Sum([remove[i-1] for i in range(1, 7)]))

# Acyclicity constraint: if both endpoints of an edge are kept,
# then the order of the source must be strictly less than the target
for (u, v) in edges:
    solver.add(Implies(And(Not(remove[u-1]), Not(remove[v-1])), order[u-1] < order[v-1]))

# Solve the optimization problem
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Collect the vertices that are removed (where remove_i is True)
    removed_vertices = [i for i in range(1, 7) if bool(model[remove[i-1]])]
    print("removed_vertices =", removed_vertices)
    # Compute the objective value (size of the feedback vertex set)
    obj_val = model.eval(Sum([remove[i-1] for i in range(1, 7)]))
    print("objective =", obj_val)
else:
    print("STATUS: unsat")