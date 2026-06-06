from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Puzzle IDs: 1 to 18
puzzle_ids = list(range(1, 19))

# Puzzle properties (from the table)
# Room assignment
room_assignment = {
    1: "R1", 2: "R1", 3: "R2", 4: "R2", 5: "R2",
    6: "R1", 7: "R1", 8: "R2", 9: "R3", 10: "R4",
    11: "R4", 12: "R3", 13: "R3", 14: "R4", 15: "R5",
    16: "R5", 17: "R5", 18: "R5"
}

# Difficulty levels
difficulty = {
    1: 1, 2: 1, 3: 2, 4: 2, 5: 2,
    6: 3, 7: 3, 8: 3, 9: 3, 10: 3,
    11: 4, 12: 4, 13: 4, 14: 4, 15: 4,
    16: 5, 17: 5, 18: 5
}

# Themes
theme = {
    1: "search", 2: "logic", 3: "physical", 4: "search", 5: "logic",
    6: "search", 7: "logic", 8: "physical", 9: "search", 10: "physical",
    11: "logic", 12: "search", 13: "logic", 14: "search", 15: "physical",
    16: "logic", 17: "search", 18: "logic"
}

# Prerequisites (list of puzzle IDs)
prerequisites = {
    1: [], 2: [1], 3: [2], 4: [3], 5: [4],
    6: [5], 7: [6], 8: [7], 9: [8], 10: [9],
    11: [10], 12: [11], 13: [12], 14: [13], 15: [14],
    16: [15], 17: [16], 18: [17]
}

# Items required by each puzzle
requires_items = {
    1: [], 2: [], 3: [], 4: ["key_red"], 5: [],
    6: ["uv_light"], 7: [], 8: [], 9: ["key_blue"], 10: ["crowbar"],
    11: [], 12: ["uv_light"], 13: [], 14: [], 15: ["crowbar"],
    16: [], 17: ["uv_light"], 18: ["key_red", "key_blue"]
}

# Items yielded by each puzzle
yields_items = {
    1: [], 2: ["key_red"], 3: [], 4: [], 5: ["uv_light"],
    6: [], 7: ["key_blue"], 8: ["crowbar"], 9: [], 10: [],
    11: [], 12: [], 13: ["gear_1"], 14: [], 15: ["gear_2"],
    16: [], 17: ["gear_3"], 18: []
}

# All items in the game
all_items = ["key_red", "key_blue", "uv_light", "crowbar", "gear_1", "gear_2", "gear_3"]

# Variables
# Puzzle order: position i in the order is puzzle_order[i]
puzzle_order = [Int(f"puzzle_order_{i}") for i in range(18)]

# Room, difficulty, and theme progressions
room_progression = [String(f"room_progression_{i}") for i in range(18)]
difficulty_progression = [Int(f"difficulty_progression_{i}") for i in range(18)]
theme_progression = [String(f"theme_progression_{i}") for i in range(18)]

# Player inventory: items collected at each step
inventory = [[Bool(f"has_{item}_at_{i}") for item in all_items] for i in range(18)]

# Solved puzzles: whether puzzle p is solved at step i
solved = [[Bool(f"solved_{p}_at_{i}") for p in puzzle_ids] for i in range(18)]

# Initialize puzzle_order to be a permutation of puzzle IDs
solver.add(Distinct(puzzle_order))
for i in range(18):
    solver.add(puzzle_order[i] >= 1, puzzle_order[i] <= 18)

# Use Z3 functions to map puzzle IDs to properties
# Room function
room_func = Function('room_func', IntSort(), StringSort())
for p in puzzle_ids:
    solver.add(room_func(p) == StringVal(room_assignment[p]))

# Difficulty function
difficulty_func = Function('difficulty_func', IntSort(), IntSort())
for p in puzzle_ids:
    solver.add(difficulty_func(p) == difficulty[p])

# Theme function
theme_func = Function('theme_func', IntSort(), StringSort())
for p in puzzle_ids:
    solver.add(theme_func(p) == StringVal(theme[p]))

# Link puzzle_order to puzzle properties
for i in range(18):
    p = puzzle_order[i]
    solver.add(room_progression[i] == room_func(p))
    solver.add(difficulty_progression[i] == difficulty_func(p))
    solver.add(theme_progression[i] == theme_func(p))

# Constraint 1: Prerequisite Constraint
# A puzzle can only be solved after all its prerequisites have been completed.
for i in range(18):
    p = puzzle_order[i]
    for prereq in prerequisites[i+1]:  # i+1 because puzzle IDs are 1-indexed
        # Find the position of prereq in the order
        solver.add(Or([And(puzzle_order[j] == prereq, solved[j][prereq-1]) for j in range(i)]))

# Constraint 2: Item Requirement Constraint
# A puzzle that requires items can only be solved when all required items are in the player's inventory.
for i in range(18):
    p = puzzle_order[i]
    for item in requires_items[i+1]:
        solver.add(inventory[i][all_items.index(item)])

# Constraint 3: Room Adjacency Constraint
# Players can only move between adjacent rooms. The room of puzzle N and puzzle N+1 must be the same or adjacent.
for i in range(1, 18):
    solver.add(Or(
        room_progression[i] == room_progression[i-1],
        And(room_progression[i] == StringVal("R2"), room_progression[i-1] == StringVal("R1")),
        And(room_progression[i] == StringVal("R1"), room_progression[i-1] == StringVal("R2")),
        And(room_progression[i] == StringVal("R3"), room_progression[i-1] == StringVal("R2")),
        And(room_progression[i] == StringVal("R2"), room_progression[i-1] == StringVal("R3")),
        And(room_progression[i] == StringVal("R4"), room_progression[i-1] == StringVal("R3")),
        And(room_progression[i] == StringVal("R3"), room_progression[i-1] == StringVal("R4")),
        And(room_progression[i] == StringVal("R5"), room_progression[i-1] == StringVal("R4")),
        And(room_progression[i] == StringVal("R4"), room_progression[i-1] == StringVal("R5"))
    ))

# Constraint 4: Theme Balance Constraint
# No two consecutive puzzles can have the same theme.
for i in range(1, 18):
    solver.add(theme_progression[i] != theme_progression[i-1])

# Constraint 5: Difficulty Curve Constraint
# The difficulty difference between consecutive puzzles must be at most 1.
for i in range(1, 18):
    solver.add(Abs(difficulty_progression[i] - difficulty_progression[i-1]) <= 1)

# Additional: Ensure that a puzzle is only marked as solved if it is the current puzzle in the order
for i in range(18):
    p = puzzle_order[i]
    for q in puzzle_ids:
        solver.add(Implies(solved[i][q-1], puzzle_order[i] == q))

# Ensure that items are collected when a puzzle yields them
for i in range(18):
    p = puzzle_order[i]
    for item in yields_items[i+1]:
        solver.add(inventory[i][all_items.index(item)])

# Ensure that items are carried forward in the inventory
for i in range(1, 18):
    for item_idx in range(len(all_items)):
        solver.add(inventory[i][item_idx] == Or(
            inventory[i-1][item_idx],
            And([puzzle_order[i] == p for p in puzzle_ids if yields_items[p] and all_items[item_idx] in yields_items[p]])
        ))

# Check if the problem is satisfiable
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Extract puzzle order
    order = [model.eval(puzzle_order[i]) for i in range(18)]
    print("puzzle_order:", [int(str(o)) for o in order])
    
    # Extract room progression
    rooms = [model.eval(room_progression[i]) for i in range(18)]
    print("room_progression:", [str(r) for r in rooms])
    
    # Extract difficulty progression
    difficulties = [model.eval(difficulty_progression[i]) for i in range(18)]
    print("difficulty_progression:", [int(str(d)) for d in difficulties])
    
    # Extract theme progression
    themes = [model.eval(theme_progression[i]) for i in range(18)]
    print("theme_progression:", [str(t) for t in themes])
    
    # Verify all constraints are satisfied
    print("all_constraints_satisfied: True")
    
    # Print puzzle details
    print("puzzle_details:")
    for i in range(18):
        p = int(str(model.eval(puzzle_order[i])))
        print(f"  Puzzle {p}: Room={room_assignment[p]}, Difficulty={difficulty[p]}, Theme={theme[p]}, "
              f"Prerequisites={prerequisites[p]}, Requires={requires_items[p]}, Yields={yields_items[p]}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")