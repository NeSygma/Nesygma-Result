from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Create solver
solver = Solver()

# Number of puzzles
N = 6

# Puzzle IDs
puzzle_ids = [1, 2, 3, 4, 5, 6]

# Difficulty levels for each puzzle
# puzzle_id -> difficulty
difficulty_map = {
    1: 1,
    2: 1,
    3: 2,
    4: 2,
    5: 3,
    6: 3
}

# Prerequisites for each puzzle
# puzzle_id -> list of prerequisite puzzle IDs
prerequisites_map = {
    1: [],
    2: [1],
    3: [2, 4],
    4: [1],
    5: [3],
    6: [5]
}

# Decision variables:
# puzzle_position[i] = position (0 to N-1) of puzzle i in the sequence
puzzle_position = [Int(f'puzzle_position_{i}') for i in puzzle_ids]

# Each puzzle must have a unique position (0 to N-1)
# This ensures each puzzle appears exactly once
solver.add(Distinct(puzzle_position))
for pos in puzzle_position:
    solver.add(pos >= 0, pos < N)

# For each puzzle, ensure its position is consistent with its prerequisites
# If puzzle j is a prerequisite for puzzle i, then position[j] < position[i]
for i in puzzle_ids:
    for j in prerequisites_map[i]:
        solver.add(puzzle_position[j-1] < puzzle_position[i-1])

# Check if the model is satisfiable
result = solver.check()

if result == sat:
    model = solver.model()
    
    # Extract puzzle order (positions sorted by puzzle_position values)
    puzzle_order = []
    for i in puzzle_ids:
        pos_val = model[puzzle_position[i-1]]
        puzzle_order.append((i, int(str(pos_val))))
    
    # Sort by position to get the sequence
    puzzle_order_sorted = sorted(puzzle_order, key=lambda x: x[1])
    puzzle_order_ids = [p[0] for p in puzzle_order_sorted]
    
    # Extract difficulty progression
    difficulty_progression = [difficulty_map[pid] for pid in puzzle_order_ids]
    
    # Verify dependencies are satisfied
    dependencies_satisfied = True
    for i in puzzle_ids:
        for j in prerequisites_map[i]:
            if model[puzzle_position[j-1]].as_long() >= model[puzzle_position[i-1]].as_long():
                dependencies_satisfied = False
                break
        if not dependencies_satisfied:
            break
    
    # Build puzzle_details array
    puzzle_details = []
    for pid in puzzle_order_ids:
        puzzle_details.append({
            'puzzle_id': pid,
            'difficulty': difficulty_map[pid],
            'prerequisites': prerequisites_map[pid]
        })
    
    print("STATUS: sat")
    print("puzzle_order:", puzzle_order_ids)
    print("difficulty_progression:", difficulty_progression)
    print("dependencies_satisfied:", dependencies_satisfied)
    print("puzzle_details:", puzzle_details)
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")