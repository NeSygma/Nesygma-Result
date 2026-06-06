from z3 import *

# Define solver
solver = Solver()

# Puzzle IDs
puzzles = [1,2,3,4,5,6]
# Difficulty mapping
difficulty_map = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3}
# Dependencies: key -> list of prerequisites
deps = {
    1: [],
    2: [1],
    3: [2,4],
    4: [1],
    5: [3],
    6: [5]
}

# Position variables for each puzzle (0..5)
pos_vars = {p: Int(f'pos_{p}') for p in puzzles}
# Domain constraints
for p in puzzles:
    solver.add(pos_vars[p] >= 0, pos_vars[p] <= 5)
# All-different constraint
solver.add(Distinct([pos_vars[p] for p in puzzles]))
# Dependency constraints: a puzzle cannot be before its prerequisites
for p, prereqs in deps.items():
    for q in prereqs:
        solver.add(pos_vars[p] > pos_vars[q])

# Check satisfiability
result = solver.check()
if result == sat:
    model = solver.model()
    # Build ordering list based on positions
    ordering = [None]*6
    for p in puzzles:
        pos_val = int(model[pos_vars[p]])
        ordering[pos_val] = p
    # Difficulty progression
    difficulty_progression = [difficulty_map[p] for p in ordering]
    # dependencies_satisfied is True
    dependencies_satisfied = True
    # Puzzle details
    puzzle_details = []
    for p in puzzles:
        puzzle_details.append({
            'puzzle_id': p,
            'difficulty': difficulty_map[p],
            'prerequisites': deps[p]
        })
    # Output
    print("STATUS: sat")
    print("puzzle_order:", ordering)
    print("difficulty_progression:", difficulty_progression)
    print("dependencies_satisfied:", dependencies_satisfied)
    print("puzzle_details:", puzzle_details)
elif result == unsat:
    print("STATUS: unsat")
else:
    print("STATUS: unknown")