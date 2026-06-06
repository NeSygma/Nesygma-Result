from z3 import *

# Define puzzles and prerequisites
puzzles = {
    1: {'difficulty': 1, 'prereq': []},
    2: {'difficulty': 1, 'prereq': [1]},
    3: {'difficulty': 2, 'prereq': [2, 4]},
    4: {'difficulty': 2, 'prereq': [1]},
    5: {'difficulty': 3, 'prereq': [3]},
    6: {'difficulty': 3, 'prereq': [5]},
}

solver = Solver()

# Position variables for each puzzle (0..5)
pos = {i: Int(f'pos_{i}') for i in puzzles}
for i in puzzles:
    solver.add(pos[i] >= 0, pos[i] <= 5)
# All positions distinct (each puzzle appears exactly once)
solver.add(Distinct([pos[i] for i in puzzles]))

# Dependency constraints: prerequisite must come earlier
for i, info in puzzles.items():
    for pre in info['prereq']:
        solver.add(pos[pre] < pos[i])

# Check satisfiability
result = solver.check()
if result == sat:
    m = solver.model()
    # Build ordering by sorting puzzles by their position
    order = sorted(puzzles.keys(), key=lambda pid: m[pos[pid]].as_long())
    difficulty_progression = [puzzles[pid]['difficulty'] for pid in order]
    dependencies_satisfied = True
    # Prepare puzzle_details list
    puzzle_details = []
    for pid in puzzles:
        puzzle_details.append({
            'puzzle_id': pid,
            'difficulty': puzzles[pid]['difficulty'],
            'prerequisites': puzzles[pid]['prereq']
        })
    print("STATUS: sat")
    print("puzzle_order =", order)
    print("difficulty_progression =", difficulty_progression)
    print("dependencies_satisfied =", dependencies_satisfied)
    print("puzzle_details =", puzzle_details)
else:
    print("STATUS: unsat")