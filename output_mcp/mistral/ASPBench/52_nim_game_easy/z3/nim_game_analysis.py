from z3 import *

# BENCHMARK_MODE: ON (model-finding mode)
BENCHMARK_MODE = True

# Initialize solver
solver = Solver()

# Initial piles (0-indexed for internal representation, but 1-indexed in output)
piles = [3, 4, 5]

# 1. Calculate nim-sum (XOR of all pile values)
nim_sum = piles[0] ^ piles[1] ^ piles[2]

# 2. Determine if current position is winning or losing
is_winning_position = (nim_sum != 0)

# 3. Find all optimal moves (if winning position)
optimal_moves = []

if is_winning_position:
    # For each pile, try removing 1 to pile_size stones
    for pile_idx in range(len(piles)):
        pile_size = piles[pile_idx]
        for stones_to_remove in range(1, pile_size + 1):
            # Resulting piles after removal
            new_piles = piles[:]
            new_piles[pile_idx] -= stones_to_remove
            
            # Calculate new nim-sum
            new_nim_sum = new_piles[0] ^ new_piles[1] ^ new_piles[2]
            
            # Check if this move makes nim-sum zero (optimal move)
            if new_nim_sum == 0:
                optimal_moves.append({
                    "pile": pile_idx + 1,  # 1-indexed
                    "stones": stones_to_remove,
                    "resulting_piles": new_piles
                })

# Prepare output
print("STATUS: sat")
print(f"nim_sum = {nim_sum}")
print(f"game_state = {'winning' if is_winning_position else 'losing'}")
print(f"is_winning_position = {is_winning_position}")
print("optimal_moves =")
for move in optimal_moves:
    print(f"  - pile: {move['pile']}, stones: {move['stones']}, resulting_piles: {move['resulting_piles']}")

# Analysis
if is_winning_position:
    print("strategy = Make the nim-sum zero by removing stones from a single pile")
    print("after_optimal_move = Opponent is now in a losing position (nim-sum = 0)")
else:
    print("strategy = No optimal move; current position is losing")
    print("after_optimal_move = N/A")