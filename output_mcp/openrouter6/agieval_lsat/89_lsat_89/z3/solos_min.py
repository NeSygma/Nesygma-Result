from z3 import *

# BENCHMARK_MODE: ON
BENCHMARK_MODE = True

# Create solver
solver = Solver()

# Positions 1..5, zero-indexed: 0->1, 1->2, 2->3, 3->4, 4->5
pianist = [Bool(f'pianist_{i}') for i in range(5)]  # True = Wayne, False = Zara
type_piece = [Bool(f'type_{i}') for i in range(5)]  # True = traditional, False = modern

# Constraint 1: third solo is traditional (index 2)
solver.add(type_piece[2] == True)

# Constraint 2: exactly one pair of consecutive traditional pieces
consecutive_trad = [If(And(type_piece[i], type_piece[i+1]), 1, 0) for i in range(4)]
solver.add(Sum(consecutive_trad) == 1)

# Constraint 3: fourth solo: pianist[3] == type_piece[3] (index 3)
solver.add(pianist[3] == type_piece[3])

# Constraint 4: pianist of second solo (index 1) != pianist of fifth solo (index 4)
solver.add(pianist[1] != pianist[4])

# Constraint 5: No traditional piece until Wayne performs at least one modern piece.
# Define wm_before[i] = whether Wayne has performed a modern piece before position i (i from 0 to 4)
wm_before = [Bool(f'wm_before_{i}') for i in range(5)]
# wm_before[0] = False (before first solo)
solver.add(wm_before[0] == False)
for i in range(1, 5):
    # wm_before[i] = wm_before[i-1] OR (pianist[i-1] AND NOT type_piece[i-1])
    solver.add(wm_before[i] == Or(wm_before[i-1], And(pianist[i-1], Not(type_piece[i-1]))))
# For each position, if it's traditional, then wm_before[i] must be True
for i in range(5):
    solver.add(Implies(type_piece[i], wm_before[i]))

# Count of Wayne's traditional pieces
count_wayne_trad = Sum([If(And(pianist[i], type_piece[i]), 1, 0) for i in range(5)])

# Find minimum k such that count_wayne_trad == k is satisfiable
min_k = None
for k in range(5):
    solver.push()
    solver.add(count_wayne_trad == k)
    if solver.check() == sat:
        min_k = k
        solver.pop()
        break
    solver.pop()

if min_k is not None:
    # Map k to letter
    letters = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    print("STATUS: sat")
    print(f"answer:{letters[min_k]}")
else:
    print("STATUS: unsat")
    print("Refine: No valid k found")