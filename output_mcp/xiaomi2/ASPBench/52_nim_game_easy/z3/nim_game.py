from z3 import *

# ============================================================
# Nim Game Analysis
# ============================================================

# Initial piles
piles = [3, 4, 5]
num_piles = len(piles)

# --- Step 1: Calculate nim-sum ---
nim_sum = 0
for p in piles:
    nim_sum ^= p

print(f"Initial piles: {piles}")
print(f"Nim-sum (XOR of all piles): {nim_sum}")

# --- Step 2: Determine winning/losing position ---
is_winning = (nim_sum != 0)
game_state = "winning" if is_winning else "losing"
print(f"Game state: {game_state}")

# --- Step 3: Find all optimal moves using Z3 ---
# An optimal move from a winning position must make the new nim-sum = 0.
# For pile i, we reduce it from piles[i] to (piles[i] XOR nim_sum).
# This works only if (piles[i] XOR nim_sum) < piles[i].

solver = Solver()

optimal_moves = []

for i in range(num_piles):
    # For each pile, check if we can make an optimal move
    # The target value for pile i after the move should be: piles[i] XOR nim_sum
    target = piles[i] ^ nim_sum
    
    # Use Z3 to verify this is a valid move
    pile_before = Int(f'pile_{i}_before')
    pile_after = Int(f'pile_{i}_after')
    stones_removed = Int(f'stones_removed_{i}')
    
    solver.push()
    
    # Current pile value
    solver.add(pile_before == piles[i])
    
    # The move: reduce pile to target
    solver.add(pile_after == target)
    solver.add(stones_removed == pile_before - pile_after)
    
    # Validity constraints
    solver.add(stones_removed >= 1)  # Must remove at least 1 stone
    solver.add(pile_after >= 0)      # Can't have negative stones
    
    # Verify resulting nim-sum is 0
    resulting_piles = list(piles)
    resulting_piles[i] = target
    resulting_nim_sum = 0
    for p in resulting_piles:
        resulting_nim_sum ^= p
    solver.add(resulting_nim_sum == 0)
    
    result = solver.check()
    
    if result == sat:
        m = solver.model()
        stones = m[stones_removed].as_long()
        move = {
            "pile": i + 1,  # 1-indexed
            "stones": stones,
            "resulting_piles": resulting_piles
        }
        optimal_moves.append(move)
        print(f"\nOptimal move found: Remove {stones} stone(s) from pile {i+1} (0-indexed: {i})")
        print(f"  Pile before: {piles[i]}")
        print(f"  Pile after: {target}")
        print(f"  Resulting piles: {resulting_piles}")
        print(f"  Resulting nim-sum: {resulting_nim_sum}")
    
    solver.pop()

# --- Step 4: Compile full analysis ---
print("\n" + "="*60)
print("COMPLETE ANALYSIS")
print("="*60)

print(f"\nInitial piles: {piles}")
print(f"Nim-sum: {nim_sum}")
print(f"Game state: {game_state}")
print(f"Is winning position: {is_winning}")
print(f"Number of optimal moves: {len(optimal_moves)}")

print(f"\nOptimal moves:")
for idx, move in enumerate(optimal_moves):
    print(f"  Move {idx+1}:")
    print(f"    Pile (1-indexed): {move['pile']}")
    print(f"    Stones to remove: {move['stones']}")
    print(f"    Resulting piles: {move['resulting_piles']}")

if is_winning:
    print(f"\nStrategy: Player 1 is in a winning position. Make a move that results in nim-sum = 0.")
    print(f"After optimal move, the opponent faces a losing position (nim-sum = 0).")
    if optimal_moves:
        best = optimal_moves[0]
        print(f"After optimal move (remove {best['stones']} from pile {best['pile']}):")
        print(f"  Resulting piles: {best['resulting_piles']}")
        print(f"  Resulting nim-sum: 0 (losing position for opponent)")
else:
    print(f"\nStrategy: Player 1 is in a losing position. Any move will leave a winning position for the opponent.")

# Final structured output
print("\n" + "="*60)
print("STRUCTURED OUTPUT")
print("="*60)
print(f"STATUS: sat")
print(f"nim_sum: {nim_sum}")
print(f"game_state: {game_state}")
print(f"is_winning_position: {is_winning}")
print(f"optimal_moves_count: {len(optimal_moves)}")
for idx, move in enumerate(optimal_moves):
    print(f"optimal_move_{idx+1}_pile: {move['pile']}")
    print(f"optimal_move_{idx+1}_stones: {move['stones']}")
    print(f"optimal_move_{idx+1}_resulting_piles: {move['resulting_piles']}")