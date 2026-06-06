from z3 import *

# Graph data
vertices = [0, 1, 2, 3, 4, 5]
edges = [(0,1), (0,2), (1,2), (1,3), (1,4), (2,1), (2,3), (2,4), (3,4), (3,5), (4,3), (4,5)]

# Convert edges to a set for quick lookup
edge_set = set(edges)

# Create solver
solver = Solver()

# Define path variables: position 0 to 5 (6 positions for 6 vertices)
path = [Int(f'pos_{i}') for i in range(6)]

# Constraint 1: Each vertex appears exactly once (permutation)
solver.add(Distinct(path))

# Constraint 2: Start at vertex 0, end at vertex 5
solver.add(path[0] == 0)
solver.add(path[5] == 5)

# Constraint 3: Consecutive vertices must have a directed edge
for i in range(5):
    # For each consecutive pair, ensure there's an edge from path[i] to path[i+1]
    edge_constraints = []
    for u, v in edge_set:
        edge_constraints.append(And(path[i] == u, path[i+1] == v))
    solver.add(Or(edge_constraints))

# Constraint 4: All vertices must be in range 0-5 (already ensured by Distinct and domain)
for i in range(6):
    solver.add(And(path[i] >= 0, path[i] <= 5))

# Find all solutions by enumeration
all_paths = []
while solver.check() == sat:
    model = solver.model()
    # Extract the path as a list of integers
    current_path = [model.eval(path[i], model_completion=True).as_long() for i in range(6)]
    all_paths.append(current_path)
    
    # Block this solution to find the next one
    # Add constraint that at least one position must differ from this solution
    block_clause = Or([path[i] != current_path[i] for i in range(6)])
    solver.add(block_clause)

# Prepare output
paths = all_paths
count = len(paths)
exists = count > 0

# Print results in required format
print("STATUS: sat")
print(f"paths = {paths}")
print(f"count = {count}")
print(f"exists = {exists}")

# Also print in a more readable format
print("\n--- Detailed Results ---")
print(f"Total Hamiltonian paths from 0 to 5: {count}")
for i, p in enumerate(paths):
    print(f"Path {i+1}: {' -> '.join(map(str, p))}")