from z3 import *

# Initial piles
initial_piles = [3, 4, 5]

# Calculate nim-sum (XOR of all pile values)
nim_sum = initial_piles[0] ^ initial_piles[1] ^ initial_piles[2]

# Determine game state
is_winning_position = nim_sum != 0

# Find optimal moves
optimal_moves = []

if is_winning_position:
    for pile_idx in range(3):
        pile_size = initial_piles[pile_idx]
        for stones_to_remove in range(1, pile_size + 1):
            # Compute new piles after removing stones_to_remove from pile_idx
            new_piles = list(initial_piles)
            new_piles[pile_idx] -= stones_to_remove
            
            # Calculate new nim-sum
            new_nim_sum = new_piles[0] ^ new_piles[1] ^ new_piles[2]
            
            # Check if the new nim-sum is 0 (optimal move)
            if new_nim_sum == 0:
                optimal_moves.append({
                    "pile": pile_idx + 1,  # 1-indexed
                    "stones": stones_to_remove,
                    "resulting_piles": new_piles
                })

# Prepare output
output = {
    "game_state": "winning" if is_winning_position else "losing",
    "optimal_moves": optimal_moves,
    "nim_sum": nim_sum,
    "analysis": {
        "is_winning_position": is_winning_position,
        "strategy": "Remove stones to make the nim-sum zero." if is_winning_position else "No optimal moves; the position is losing.",
        "after_optimal_move": "The opponent is forced into a losing position." if is_winning_position and optimal_moves else "No move can force the opponent into a losing position."
    }
}

# Print output
print("STATUS: sat")
print(f"game_state: {output['game_state']}")
print(f"nim_sum: {output['nim_sum']}")
print("optimal_moves:")
for move in output['optimal_moves']:
    print(f"  - pile: {move['pile']}, stones: {move['stones']}, resulting_piles: {move['resulting_piles']}")
print("analysis:")
print(f"  is_winning_position: {output['analysis']['is_winning_position']}")
print(f"  strategy: {output['analysis']['strategy']}")
print(f"  after_optimal_move: {output['analysis']['after_optimal_move']}")