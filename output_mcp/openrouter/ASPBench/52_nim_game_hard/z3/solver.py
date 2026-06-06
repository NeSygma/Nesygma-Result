from z3 import *
import itertools, sys

# Initial data
initial = [6,7,10,13]
initial_nim_sum = 0
for v in initial:
    initial_nim_sum ^= v

# Helper to compute nim-sum using Python (for quick check)
def nim_sum(piles):
    s = 0
    for v in piles:
        s ^= v
    return s

optimal_moves = []

# Enumerate standard moves
for i, size in enumerate(initial):
    for r in range(1, size+1):
        new_size = size - r
        new_piles = [p for j,p in enumerate(initial) if j != i]
        if new_size > 0:
            new_piles.append(new_size)
        # distinct sizes constraint
        if len(set(new_piles)) != len(new_piles):
            continue
        # Use Z3 to enforce xor == 0
        solver = Solver()
        # create BitVec constants for each pile
        bv = [BitVecVal(v, 32) for v in new_piles]
        # distinct
        solver.add(Distinct(bv))
        # xor zero
        xor_expr = bv[0]
        for b in bv[1:]:
            xor_expr = xor_expr ^ b
        solver.add(xor_expr == 0)
        if solver.check() == sat:
            move = {
                "move_type": "standard",
                "pile_index": i,
                "stones_removed": r,
                "split_into": None,
                "resulting_piles": sorted(new_piles)
            }
            optimal_moves.append(move)

# Enumerate split moves (player 1 power)
for i, size in enumerate(initial):
    if size % 2 != 0:
        continue
    # generate unordered splits a <= b
    for a in range(1, size//2 + 1):
        b = size - a
        if a > b:
            continue
        new_piles = [p for j,p in enumerate(initial) if j != i] + [a, b]
        if len(set(new_piles)) != len(new_piles):
            continue
        solver = Solver()
        bv = [BitVecVal(v, 32) for v in new_piles]
        solver.add(Distinct(bv))
        xor_expr = bv[0]
        for bvv in bv[1:]:
            xor_expr = xor_expr ^ bvv
        solver.add(xor_expr == 0)
        if solver.check() == sat:
            move = {
                "move_type": "power_split",
                "pile_index": i,
                "stones_removed": None,
                "split_into": [a, b],
                "resulting_piles": sorted(new_piles)
            }
            optimal_moves.append(move)

# Output
print("STATUS: sat")
print(f"initial_nim_sum = {initial_nim_sum}")
print(f"is_winning_position = {initial_nim_sum != 0}")
print("optimal_moves:")
for mv in optimal_moves:
    print(mv)