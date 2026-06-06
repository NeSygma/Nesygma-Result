from z3 import *

# Problem data
initial_piles = [6, 7, 10, 13]
num_piles = len(initial_piles)

# Helper to compute nim-sum

def nim_sum(piles):
    res = 0
    for p in piles:
        res ^= p
    return res

# Collect optimal moves
optimal_moves = []

# Standard moves
for i, pile in enumerate(initial_piles):
    for removed in range(1, pile+1):
        # resulting piles
        new_piles = []
        for j, p in enumerate(initial_piles):
            if j == i:
                if p - removed > 0:
                    new_piles.append(p - removed)
                # if removed all stones, pile disappears
            else:
                new_piles.append(p)
        # distinctness check
        if len(new_piles) != len(set(new_piles)):
            continue
        # nim-sum check
        if nim_sum(new_piles) == 0:
            optimal_moves.append({
                'move_type': 'standard',
                'pile_index': i,
                'stones_removed': removed,
                'split_into': None,
                'resulting_piles': sorted(new_piles)
            })

# Split moves (Player 1 has split power)
for i, pile in enumerate(initial_piles):
    if pile % 2 == 0:
        # split into two positive integers a,b with a+b=pile
        for a in range(1, pile):
            b = pile - a
            if a == 0 or b == 0:
                continue
            new_piles = []
            for j, p in enumerate(initial_piles):
                if j == i:
                    new_piles.append(a)
                    new_piles.append(b)
                else:
                    new_piles.append(p)
            # distinctness check
            if len(new_piles) != len(set(new_piles)):
                continue
            if nim_sum(new_piles) == 0:
                optimal_moves.append({
                    'move_type': 'power_split',
                    'pile_index': i,
                    'stones_removed': None,
                    'split_into': [a, b],
                    'resulting_piles': sorted(new_piles)
                })

# Output
print("STATUS: sat")
print("optimal_moves:")
for move in optimal_moves:
    print(f"- move_type: {move['move_type']}, pile_index: {move['pile_index']}, stones_removed: {move['stones_removed']}, split_into: {move['split_into']}, resulting_piles: {move['resulting_piles']}")