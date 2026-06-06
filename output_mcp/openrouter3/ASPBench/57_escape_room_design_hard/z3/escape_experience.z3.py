from z3 import *

# Problem data
puzzles = {
    1: {"room": "R1", "difficulty": 1, "theme": "search", "prereqs": [], "requires": [], "yields": []},
    2: {"room": "R1", "difficulty": 1, "theme": "logic", "prereqs": [1], "requires": [], "yields": ["key_red"]},
    3: {"room": "R2", "difficulty": 2, "theme": "physical", "prereqs": [2], "requires": [], "yields": []},
    4: {"room": "R2", "difficulty": 2, "theme": "search", "prereqs": [3], "requires": ["key_red"], "yields": []},
    5: {"room": "R2", "difficulty": 2, "theme": "logic", "prereqs": [4], "requires": [], "yields": ["uv_light"]},
    6: {"room": "R1", "difficulty": 3, "theme": "search", "prereqs": [5], "requires": ["uv_light"], "yields": []},
    7: {"room": "R1", "difficulty": 3, "theme": "logic", "prereqs": [6], "requires": [], "yields": ["key_blue"]},
    8: {"room": "R2", "difficulty": 3, "theme": "physical", "prereqs": [7], "requires": [], "yields": ["crowbar"]},
    9: {"room": "R3", "difficulty": 3, "theme": "search", "prereqs": [8], "requires": ["key_blue"], "yields": []},
    10: {"room": "R4", "difficulty": 3, "theme": "physical", "prereqs": [9], "requires": ["crowbar"], "yields": []},
    11: {"room": "R4", "difficulty": 4, "theme": "logic", "prereqs": [10], "requires": [], "yields": []},
    12: {"room": "R3", "difficulty": 4, "theme": "search", "prereqs": [11], "requires": ["uv_light"], "yields": []},
    13: {"room": "R3", "difficulty": 4, "theme": "logic", "prereqs": [12], "requires": [], "yields": ["gear_1"]},
    14: {"room": "R4", "difficulty": 4, "theme": "search", "prereqs": [13], "requires": [], "yields": []},
    15: {"room": "R5", "difficulty": 4, "theme": "physical", "prereqs": [14], "requires": ["crowbar"], "yields": ["gear_2"]},
    16: {"room": "R5", "difficulty": 5, "theme": "logic", "prereqs": [15], "requires": [], "yields": []},
    17: {"room": "R5", "difficulty": 5, "theme": "search", "prereqs": [16], "requires": ["uv_light"], "yields": ["gear_3"]},
    18: {"room": "R5", "difficulty": 5, "theme": "logic", "prereqs": [17], "requires": ["key_red", "key_blue"], "yields": []}
}

# Room adjacency mapping
room_adjacency = {
    "R1": ["R1", "R2"],
    "R2": ["R1", "R2", "R3"],
    "R3": ["R2", "R3", "R4"],
    "R4": ["R3", "R4", "R5"],
    "R5": ["R4", "R5"]
}

# Theme mapping
themes = ["search", "logic", "physical"]

# Create solver
solver = Solver()

# Decision variables: position of each puzzle in the ordering (1 to 18)
puzzle_position = [Int(f"pos_{i}") for i in range(1, 19)]

# All positions must be distinct and in range 1-18
for i in range(18):
    solver.add(puzzle_position[i] >= 1)
    solver.add(puzzle_position[i] <= 18)
solver.add(Distinct(puzzle_position))

# Create reverse mapping: position -> puzzle
position_to_puzzle = [Int(f"puz_at_pos_{j}") for j in range(1, 19)]
for j in range(18):
    solver.add(position_to_puzzle[j] >= 1)
    solver.add(position_to_puzzle[j] <= 18)
solver.add(Distinct(position_to_puzzle))

# Link position and puzzle variables
for i in range(18):
    puzzle_id = i + 1
    for j in range(18):
        # If puzzle i is at position j+1, then position_to_puzzle[j] = puzzle_id
        solver.add(Implies(puzzle_position[i] == j + 1, position_to_puzzle[j] == puzzle_id))

# Constraint 1: Prerequisite constraint
# For each puzzle, all its prerequisites must come before it
for puzzle_id in range(1, 19):
    prereqs = puzzles[puzzle_id]["prereqs"]
    for prereq in prereqs:
        # prereq must come before puzzle_id
        solver.add(puzzle_position[prereq - 1] < puzzle_position[puzzle_id - 1])

# Constraint 2: Item requirement constraint
# We need to track when items become available
# Items are yielded by puzzles and required by others
# For each puzzle that requires items, all yielding puzzles must come before it

# Map items to the puzzles that yield them
item_yielders = {
    "key_red": [2],
    "key_blue": [7],
    "uv_light": [5],
    "crowbar": [8],
    "gear_1": [13],
    "gear_2": [15],
    "gear_3": [17]
}

# For each puzzle that requires items, ensure all yielders come before it
for puzzle_id in range(1, 19):
    required_items = puzzles[puzzle_id]["requires"]
    for item in required_items:
        for yielder in item_yielders[item]:
            solver.add(puzzle_position[yielder - 1] < puzzle_position[puzzle_id - 1])

# Constraint 3: Room adjacency constraint
# Room of puzzle N and puzzle N+1 must be same or adjacent
for pos in range(17):  # positions 1-17
    puzzle1 = position_to_puzzle[pos]  # puzzle at position pos+1
    puzzle2 = position_to_puzzle[pos + 1]  # puzzle at position pos+2
    
    # For each possible pair of puzzles, check if they can be adjacent
    # We need to encode: if puzzle1 = p1 and puzzle2 = p2, then rooms must be adjacent
    for p1 in range(1, 19):
        for p2 in range(1, 19):
            room1 = puzzles[p1]["room"]
            room2 = puzzles[p2]["room"]
            adjacent = room2 in room_adjacency[room1]
            solver.add(Implies(And(puzzle1 == p1, puzzle2 == p2), adjacent))

# Constraint 4: Theme balance constraint
# No two consecutive puzzles can have the same theme
for pos in range(17):
    puzzle1 = position_to_puzzle[pos]
    puzzle2 = position_to_puzzle[pos + 1]
    
    for p1 in range(1, 19):
        for p2 in range(1, 19):
            theme1 = puzzles[p1]["theme"]
            theme2 = puzzles[p2]["theme"]
            solver.add(Implies(And(puzzle1 == p1, puzzle2 == p2), theme1 != theme2))

# Constraint 5: Difficulty curve constraint
# Difficulty difference between consecutive puzzles must be at most 1
for pos in range(17):
    puzzle1 = position_to_puzzle[pos]
    puzzle2 = position_to_puzzle[pos + 1]
    
    for p1 in range(1, 19):
        for p2 in range(1, 19):
            diff1 = puzzles[p1]["difficulty"]
            diff2 = puzzles[p2]["difficulty"]
            solver.add(Implies(And(puzzle1 == p1, puzzle2 == p2), Abs(diff1 - diff2) <= 1))

# Check for solution
result = solver.check()

if result == sat:
    model = solver.model()
    
    # Extract ordering
    puzzle_order = []
    for pos in range(18):
        puzzle_at_pos = model[position_to_puzzle[pos]].as_long()
        puzzle_order.append(puzzle_at_pos)
    
    # Extract room progression
    room_progression = [puzzles[p]["room"] for p in puzzle_order]
    
    # Extract difficulty progression
    difficulty_progression = [puzzles[p]["difficulty"] for p in puzzle_order]
    
    # Extract theme progression
    theme_progression = [puzzles[p]["theme"] for p in puzzle_order]
    
    # Verify all constraints are satisfied
    all_constraints_satisfied = True
    
    # Check prerequisite constraint
    for puzzle_id in range(1, 19):
        prereqs = puzzles[puzzle_id]["prereqs"]
        for prereq in prereqs:
            if puzzle_order.index(prereq) >= puzzle_order.index(puzzle_id):
                all_constraints_satisfied = False
    
    # Check item constraint
    for puzzle_id in range(1, 19):
        required_items = puzzles[puzzle_id]["requires"]
        for item in required_items:
            for yielder in item_yielders[item]:
                if puzzle_order.index(yielder) >= puzzle_order.index(puzzle_id):
                    all_constraints_satisfied = False
    
    # Check room adjacency
    for i in range(17):
        room1 = room_progression[i]
        room2 = room_progression[i + 1]
        if room2 not in room_adjacency[room1]:
            all_constraints_satisfied = False
    
    # Check theme balance
    for i in range(17):
        if theme_progression[i] == theme_progression[i + 1]:
            all_constraints_satisfied = False
    
    # Check difficulty curve
    for i in range(17):
        if abs(difficulty_progression[i] - difficulty_progression[i + 1]) > 1:
            all_constraints_satisfied = False
    
    print("STATUS: sat")
    print(f"puzzle_order: {puzzle_order}")
    print(f"room_progression: {room_progression}")
    print(f"difficulty_progression: {difficulty_progression}")
    print(f"theme_progression: {theme_progression}")
    print(f"all_constraints_satisfied: {all_constraints_satisfied}")
    print("\npuzzle_details:")
    for p in puzzle_order:
        print(f"  Puzzle {p}: Room={puzzles[p]['room']}, Difficulty={puzzles[p]['difficulty']}, Theme={puzzles[p]['theme']}")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No valid ordering found that satisfies all constraints")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")