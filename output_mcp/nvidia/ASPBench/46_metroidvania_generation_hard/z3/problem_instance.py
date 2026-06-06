from z3 import *

solver = Solver()

# Define edges
edges = [
    ("Start", "R1"),
    ("R1", "Start"),
    ("R1", "R2"),
    ("R2", "R1"),
    ("R2", "R3"),
    ("R3", "R2"),
    ("R3", "R4"),
    ("R4", "R3"),
    ("R4", "R5"),
    ("R5", "R4"),
    ("R5", "R6"),
    ("R6", "R5"),
    ("R6", "R7"),
    ("R7", "R6"),
    ("R7", "R8"),
    ("R8", "R7"),
    ("R8", "R9"),
    ("R9", "R8"),
    ("R9", "R10"),
    ("R10", "R9"),
    ("R10", "Goal"),
    ("R1", "R3")
]

# Create requires variables
req_vars = [Int(f"req_{i}") for i in range(len(edges))]

# Domain constraints for requires: 0..4
for r in req_vars:
    solver.add(r >= 0, r <= 4)

# Bidirectional pairs indices
bidir_pairs = [(0,1),(2,3),(4,5),(6,7),(8,9),(10,11),(12,13),(14,15),(16,17),(18,19)]

# Add constraints: for each pair, at least one direction is null (0)
for i,j in bidir_pairs:
    solver.add(Or(req_vars[i] == 0, req_vars[j] == 0))

# Location variables (indices 0..9)
flooded_room_idx = Int('flooded_room_idx')
chasm_room_idx = Int('chasm_room_idx')
red_key_loc_idx = Int('red_key_loc_idx')
blue_key_loc_idx = Int('blue_key_loc_idx')
green_key_loc_idx = Int('green_key_loc_idx')
yellow_key_loc_idx = Int('yellow_key_loc_idx')
boots_loc_idx = Int('boots_loc_idx')
grapple_loc_idx = Int('grapple_loc_idx')

# Domain constraints for location indices: 0..9
for var in [flooded_room_idx, chasm_room_idx, red_key_loc_idx, blue_key_loc_idx,
            green_key_loc_idx, yellow_key_loc_idx, boots_loc_idx, grapple_loc_idx]:
    solver.add(var >= 0, var <= 9)

# Constraints
solver.add(flooded_room_idx != chasm_room_idx)  # distinct special rooms
solver.add(boots_loc_idx != flooded_room_idx)  # Boots not in Flooded
solver.add(grapple_loc_idx != chasm_room_idx)  # Grapple not in Chasm
solver.add(yellow_key_loc_idx == chasm_room_idx)  # YellowKey in Chasm

# BENCHMARK_MODE
BENCHMARK_MODE = True

# Check satisfiability
result = solver.check()

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    # Print some model values
    print("flooded_room_idx =", model.evaluate(flooded_room_idx))
    print("chasm_room_idx =", model.evaluate(chasm_room_idx))
    print("yellow_key_loc_idx =", model.evaluate(yellow_key_loc_idx))
    print("boots_loc_idx =", model.evaluate(boots_loc_idx))
    print("grapple_loc_idx =", model.evaluate(grapple_loc_idx))
    # Print some requires values for illustration
    print("requires_Start_R1 =", model.evaluate(req_vars[0]))
    print("requires_R10_Goal =", model.evaluate(req_vars[20]))
    # Print all requires values for completeness
    for i, r in enumerate(req_vars):
        print(f"requires_{i} =", model.evaluate(r))
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")