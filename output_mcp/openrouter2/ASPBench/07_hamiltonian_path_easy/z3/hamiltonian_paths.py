from z3 import *

# Problem data
vertices = [0,1,2,3,4,5]
edges = [(0,1),(0,2),(1,2),(1,3),(1,4),(2,1),(2,3),(2,4),(3,4),(3,5),(4,3),(4,5)]
start = 0
end = 5
n = len(vertices)

# Declare position variables: pos[i] is the vertex at position i in the path
pos = [Int(f'pos_{i}') for i in range(n)]

solver = Solver()
# Domain constraints
for p in pos:
    solver.add(p >= 0, p <= 5)
# All vertices must be distinct
solver.add(Distinct(pos))
# Start and end constraints
solver.add(pos[0] == start)
solver.add(pos[n-1] == end)
# Adjacency constraints for each consecutive pair
for i in range(n-1):
    allowed = []
    for (u,v) in edges:
        allowed.append(And(pos[i] == u, pos[i+1] == v))
    solver.add(Or(allowed))

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    path = [m[pos[i]].as_long() for i in range(n)]
    solutions.append(path)
    # Block this solution
    solver.add(Or([pos[i] != m[pos[i]] for i in range(n)]))

count = len(solutions)
exists = count > 0

# Output results
if exists:
    print("STATUS: sat")
else:
    print("STATUS: unsat")
print("paths:", solutions)
print("count:", count)
print("exists:", exists)