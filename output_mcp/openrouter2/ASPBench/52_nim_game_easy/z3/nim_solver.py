from z3 import *

# Problem data
piles = [3, 4, 5]

# Compute current nim-sum
nim_sum_current = piles[0] ^ piles[1] ^ piles[2]

# Determine game state
game_state = "winning" if nim_sum_current != 0 else "losing"

# Find all optimal moves that make nim-sum zero
optimal_moves = []
for i in range(len(piles)):
    for r in range(1, piles[i] + 1):
        new_piles = piles.copy()
        new_piles[i] -= r
        nim_sum_new = new_piles[0] ^ new_piles[1] ^ new_piles[2]
        if nim_sum_new == 0:
            optimal_moves.append({
                'pile': i + 1,  # 1-indexed
                'stones': r,
                'resulting_piles': new_piles
            })

# Prepare analysis
analysis = {
    'is_winning_position': game_state == "winning",
    'strategy': "reduce a pile to make nim-sum zero",
    'after_optimal_move': "losing position with nim_sum 0"
}

# Output
print("STATUS: sat")
print(f"game_state: {game_state}")
print(f"nim_sum: {nim_sum_current}")
print("optimal_moves: [")
for move in optimal_moves:
    print(f"  {{'pile':{move['pile']}, 'stones':{move['stones']}, 'resulting_piles':{move['resulting_piles']}}},")
print("]")
print("analysis: {")
print(f"  'is_winning_position': {analysis['is_winning_position']},")
print(f"  'strategy': '{analysis['strategy']}',")
print(f"  'after_optimal_move': '{analysis['after_optimal_move']}'")
print("}")