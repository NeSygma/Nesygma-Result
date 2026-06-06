from z3 import *

solver = Solver()

# Removal variables
r0 = Int('r0')
r1 = Int('r1')
r2 = Int('r2')

# Exactly one removal, within bounds
solver.add(Or(And(r0 >= 1, r0 <= 3), And(r1 >= 1, r1 <= 4), And(r2 >= 1, r2 <= 5)))
solver.add(Or(r0 == 0, r1 == 0))
solver.add(Or(r0 == 0, r2 == 0))
solver.add(Or(r1 == 0, r2 == 0))

# Nim-sum condition for resulting position
solver.add((3 - r0) ^ (4 - r1) ^ (5 - r2) == 0)

# BENCHMARK_MODE = True (model-finding)
BENCHMARK_MODE = True

# Collect optimal moves
optimal_moves = []

while True:
    result = solver.check()
    if result != sat:
        break
    m = solver.model()
    # Extract removal values
    rv0 = m[r0].as_long()
    rv1 = m[r1].as_long()
    rv2 = m[r2].as_long()
    # Find which pile is reduced
    for i, rv in enumerate([rv0, rv1, rv2]):
        if rv > 0:
            pile = i + 1
            stones = rv
            resulting = [3, 4, 5]
            resulting[i] = resulting[i] - stones
            optimal_moves.append((pile, stones, resulting))
            # Block this move
            block = Or(r0 != rv0, r1 != rv1, r2 != rv2)
            solver.add(block)
            break

# Print results
if optimal_moves:
    print("STATUS: sat")
    # nim_sum of original position
    nim_sum_val = 3 ^ 4 ^ 5
    print(f"nim_sum = {nim_sum_val}")
    print(f"game_state = {'winning' if nim_sum_val != 0 else 'losing'}")
    print(f"optimal_moves = {optimal_moves}")
    # analysis fields
    print("analysis.is_winning_position = True")
    print('analysis.strategy = "Make nim-sum zero"')
    # after move analysis: use the resulting piles of the first optimal move
    if optimal_moves:
        resulting_piles = optimal_moves[0][2]
        print(f'analysis.after_optimal_move = "Resulting piles {resulting_piles}"')
else:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")