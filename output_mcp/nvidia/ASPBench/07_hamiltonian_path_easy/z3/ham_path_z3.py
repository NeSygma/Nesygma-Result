from z3 import *

edges = [(0,1),(0,2),(1,2),(1,3),(1,4),(2,1),(2,3),(2,4),(3,4),(3,5),(4,3),(4,5)]

order = [Int(f'p{i}') for i in range(6)]
solver = Solver()

# domain
for v in order:
    solver.add(v >= 0, v < 6)

# all different
solver.add(Distinct(order))

# start and end
solver.add(order[0] == 0)
solver.add(order[5] == 5)

# consecutive edge constraints
for i in range(5):
    solver.add(Or([And(order[i] == u, order[i+1] == v) for (u,v) in edges]))

solutions = []
while solver.check() == sat:
    m = solver.model()
    path = [m.eval(order[i]).as_long() for i in range(6)]
    solutions.append(path)
    # block this exact solution
    solver.add(Or([order[i] != path[i] for i in range(6)]))

if len(solutions) == 0:
    print("STATUS: unsat")
else:
    print("STATUS: sat")
    print("paths =", solutions)
    print("count =", len(solutions))
    print("exists =", len(solutions) > 0)