from z3 import *

solver = Solver()

# Position variables for each puzzle (1-indexed)
pos = [None] + [Int(f'pos_{i}') for i in range(1,7)]

# All positions must be distinct (bijection to 0..5)
solver.add(Distinct(*pos[1:]))

# Dependency constraints: prerequisite must come before dependent
solver.add(pos[2] > pos[1])  # 1 -> 2
solver.add(pos[3] > pos[2])  # 2 -> 3
solver.add(pos[3] > pos[4])  # 4 -> 3
solver.add(pos[4] > pos[1])  # 1 -> 4
solver.add(pos[5] > pos[3])  # 3 -> 5
solver.add(pos[6] > pos[5])  # 5 -> 6

# Check for a solution
result = solver.check()
if result == sat:
    print("STATUS: sat")
    model = solver.model()
    # Extract position of each puzzle
    puzzle_pos = {}
    for p in range(1,7):
        puzzle_pos[p] = model.eval(pos[p]).as_long()
    # Build ordering list: index = position, value = puzzle id
    order = [None] * 6
    for p in range(1,7):
        position = puzzle_pos[p]
        order[position] = p
    print("puzzle_order:", order)
    # Difficulty mapping
    difficulty = {1:1, 2:1, 3:2, 4:2, 5:3, 6:3}
    difficulty_progression = [difficulty[p] for p in order]
    print("difficulty_progression:", difficulty_progression)
    print("dependencies_satisfied: True")
    # Puzzle details (static)
    puzzle_details = []
    for pid in range(1,7):
        if pid == 1:
            prereq = []
        elif pid == 2:
            prereq = [1]
        elif pid == 3:
            prereq = [2,4]
        elif pid == 4:
            prereq = [1]
        elif pid == 5:
            prereq = [3]
        elif pid == 6:
            prereq = [5]
        else:
            prereq = []
        puzzle_details.append({
            "puzzle_id": pid,
            "difficulty": difficulty[pid],
            "prerequisites": prereq
        })
    print("puzzle_details:", puzzle_details)
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error; refine required)")
else:
    print("STATUS: unknown")