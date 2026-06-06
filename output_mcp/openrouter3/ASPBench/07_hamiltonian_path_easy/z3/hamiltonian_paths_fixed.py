from z3 import *

# Problem parameters
N = 6  # Number of vertices
start = 0
end = 5

# Directed edges as given
edges = [(0,1), (0,2), (1,2), (1,3), (1,4), (2,1), (2,3), (2,4), (3,4), (3,5), (4,3), (4,5)]

# Create a solver
solver = Solver()

# Decision variables: position[i] = vertex at position i in the path
# We need N positions (0 to N-1) for N vertices
position = [Int(f'pos_{i}') for i in range(N)]

# Add domain constraints: each position must be a vertex 0-5
for i in range(N):
    solver.add(position[i] >= 0)
    solver.add(position[i] < N)

# Constraint 1: Each vertex appears exactly once (all vertices are distinct)
solver.add(Distinct(position))

# Constraint 2: Path must start at vertex 0 and end at vertex 5
solver.add(position[0] == start)
solver.add(position[N-1] == end)

# Constraint 3: Path must follow directed edges
# For each consecutive pair in the path, there must be a directed edge
for i in range(N-1):
    # Create a constraint that (position[i], position[i+1]) must be in edges
    edge_constraints = []
    for (u, v) in edges:
        edge_constraints.append(And(position[i] == u, position[i+1] == v))
    solver.add(Or(edge_constraints))

# Find all solutions
solutions = []
while solver.check() == sat:
    model = solver.model()
    # Extract the path
    path = [model.eval(position[i], model_completion=True) for i in range(N)]
    # Convert to Python integers
    path_ints = [int(str(v)) for v in path]
    solutions.append(path_ints)
    
    # Add blocking clause to find different solutions
    # We need to ensure at least one position has a different value
    blocking_clause = Or([position[i] != model.eval(position[i], model_completion=True) for i in range(N)])
    solver.add(blocking_clause)

# Prepare output
paths = solutions
count = len(paths)
exists = count > 0

# Print results
print("STATUS: sat")
print(f"paths = {paths}")
print(f"count = {count}")
print(f"exists = {exists}")

# Also print in a more structured format
print("\nDetailed results:")
print(f"Total Hamiltonian paths from {start} to {end}: {count}")
for i, path in enumerate(paths):
    print(f"Path {i+1}: {' -> '.join(map(str, path))}")

# Verify each path against the graph edges
print("\nVerification:")
for i, path in enumerate(paths):
    valid = True
    for j in range(len(path)-1):
        if (path[j], path[j+1]) not in edges:
            valid = False
            print(f"Path {i+1} INVALID: edge ({path[j]}, {path[j+1]}) not in graph")
    if valid:
        print(f"Path {i+1} VALID")