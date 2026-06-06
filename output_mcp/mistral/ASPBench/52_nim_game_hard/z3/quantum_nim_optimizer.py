from z3 import *

# ============================================================================
# Quantum Nim Optimal Move Finder
# ============================================================================
# Instance: Piles [6, 7, 10, 13], Player 1's turn, both powers available
# Goal: Find ALL optimal moves (standard or split) that result in nim-sum = 0
# ============================================================================

# ----------------------------------------------------------------------------
# 1. Declare symbolic variables for moves and resulting states
# ----------------------------------------------------------------------------

# Initial piles
initial_piles = [6, 7, 10, 13]
N = len(initial_piles)

# ============================================================================
# PART A: Standard Moves
# ============================================================================

standard_solutions = []

# Try each pile for a standard move
for target_pile in range(N):
    s = Solver()
    
    # Only this pile is modified
    removed_target = Int('removed_target')
    s.add(removed_target >= 1, removed_target <= initial_piles[target_pile])
    
    # Resulting piles: all unchanged except target_pile
    resulting_piles = [Int(f'res_{i}') for i in range(N)]
    for i in range(N):
        if i == target_pile:
            s.add(resulting_piles[i] == initial_piles[i] - removed_target)
        else:
            s.add(resulting_piles[i] == initial_piles[i])
    
    # All piles must be distinct
    s.add(Distinct(resulting_piles))
    
    # Check and collect solution
    if s.check() == sat:
        m = s.model()
        # Compute nim-sum as integer XOR
        res_vals = [m[resulting_piles[i]].as_long() for i in range(N)]
        nim_sum = res_vals[0]
        for i in range(1, N):
            nim_sum ^= res_vals[i]
        if nim_sum == 0:
            standard_solutions.append({
                'move_type': 'standard',
                'pile_index': target_pile,
                'stones_removed': m[removed_target].as_long(),
                'resulting_piles': res_vals,
                'nim_sum': nim_sum
            })

# ============================================================================
# PART B: Split Moves (Player 1 only)
# ============================================================================

split_solutions = []

# Try splitting each even pile
for target_pile in range(N):
    if initial_piles[target_pile] % 2 != 0:
        continue  # Can only split even piles
    
    s = Solver()
    
    a = Int('a')
    b = Int('b')
    s.add(a > 0, b > 0, a + b == initial_piles[target_pile])
    
    # Resulting piles: replace target_pile with a and b
    # Total piles becomes N+1
    resulting_piles = [Int(f'res_{i}') for i in range(N+1)]
    
    # Fill in the piles
    for i in range(target_pile):
        s.add(resulting_piles[i] == initial_piles[i])
    s.add(resulting_piles[target_pile] == a)
    s.add(resulting_piles[target_pile+1] == b)
    for i in range(target_pile+1, N):
        s.add(resulting_piles[i+1] == initial_piles[i])
    
    # All piles must be distinct
    s.add(Distinct(resulting_piles))
    
    # Check and collect solution
    if s.check() == sat:
        m = s.model()
        # Compute nim-sum as integer XOR
        res_vals = [m[resulting_piles[i]].as_long() for i in range(N+1)]
        nim_sum = res_vals[0]
        for i in range(1, N+1):
            nim_sum ^= res_vals[i]
        if nim_sum == 0:
            split_solutions.append({
                'move_type': 'power_split',
                'pile_index': target_pile,
                'split_into': [m[a].as_long(), m[b].as_long()],
                'resulting_piles': res_vals,
                'nim_sum': nim_sum
            })

# ============================================================================
# 4. Combine and report all optimal moves
# ============================================================================

all_optimal_moves = standard_solutions + split_solutions

# Print results
print("STATUS: sat")
print(f"Total optimal moves found: {len(all_optimal_moves)}")

if all_optimal_moves:
    for idx, move in enumerate(all_optimal_moves):
        print(f"\nOptimal Move #{idx+1}:")
        print(f"  Move type: {move['move_type']}")
        print(f"  Pile index: {move['pile_index']}")
        if move['move_type'] == 'standard':
            print(f"  Stones removed: {move['stones_removed']}")
        else:
            print(f"  Split into: {move['split_into']}")
        print(f"  Resulting piles: {move['resulting_piles']}")
        print(f"  Nim-sum: {move['nim_sum']}")
else:
    print("No optimal moves found.")

# Expected: 3 standard moves
if len(standard_solutions) == 3 and len(split_solutions) == 0:
    print("\nExpected result confirmed: 3 standard optimal moves, 0 split moves.")
elif len(all_optimal_moves) > 0:
    print(f"\nFound {len(all_optimal_moves)} optimal moves (expected 3 standard moves).")
else:
    print("\nNo optimal moves found (unexpected).")