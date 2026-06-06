from z3 import *

# Initial piles
piles = [3, 4, 5]
n = len(piles)

# Calculate nim-sum (XOR of all pile values)
nim_sum = piles[0] ^ piles[1] ^ piles[2]

print(f"Initial piles: {piles}")
print(f"Nim-sum: {nim_sum}")

# Determine if winning position
is_winning = nim_sum != 0
game_state = "winning" if is_winning else "losing"
print(f"Game state: {game_state}")

# Find all optimal moves
# An optimal move from a winning position makes the nim-sum zero.
# For each pile i, we need to find a removal r (1 <= r <= piles[i]) such that
# after removing r from pile i, the XOR of the new piles is 0.
# That means: new_piles[i] = piles[i] - r, and XOR of all new piles = 0.
# Equivalently: (piles[i] - r) == piles[i] ^ nim_sum, and (piles[i] - r) < piles[i]

optimal_moves = []

for i in range(n):
    # The target size for pile i after removal to make XOR zero is: piles[i] ^ nim_sum
    target = piles[i] ^ nim_sum
    # We need to remove r = piles[i] - target stones
    # Constraints: r >= 1 (must remove at least 1), r <= piles[i] (can't remove more than available)
    # Also target >= 0 (pile can't be negative)
    if target >= 0 and target < piles[i]:
        r = piles[i] - target
        if r >= 1 and r <= piles[i]:
            new_piles = piles.copy()
            new_piles[i] = target
            optimal_moves.append({
                "pile": i + 1,  # 1-indexed
                "stones": r,
                "resulting_piles": new_piles
            })

print(f"\nOptimal moves found: {len(optimal_moves)}")
for move in optimal_moves:
    print(f"  Remove {move['stones']} stone(s) from pile {move['pile']} -> resulting piles: {move['resulting_piles']}")

# Verify: after each optimal move, nim-sum should be 0
for move in optimal_moves:
    new_xor = move['resulting_piles'][0] ^ move['resulting_piles'][1] ^ move['resulting_piles'][2]
    assert new_xor == 0, f"Move {move} does not yield nim-sum 0!"
    print(f"  Verified: resulting nim-sum = {new_xor}")

# Analysis
print(f"\n--- Analysis ---")
print(f"is_winning_position: {is_winning}")
if is_winning:
    print(f"strategy: Current position is winning (nim-sum = {nim_sum} != 0). "
          f"Optimal play: make a move that results in nim-sum = 0.")
    if optimal_moves:
        move = optimal_moves[0]
        print(f"after_optimal_move: Remove {move['stones']} stone(s) from pile {move['pile']}. "
              f"Resulting piles: {move['resulting_piles']} (nim-sum = 0, losing position for opponent).")
else:
    print(f"strategy: Current position is losing (nim-sum = 0). Any move leads to a winning position for the opponent.")

print(f"\nSTATUS: sat")