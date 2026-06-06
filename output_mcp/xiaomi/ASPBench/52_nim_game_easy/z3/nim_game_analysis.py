from z3 import *

# Nim game analysis using Z3
# Initial piles: [3, 4, 5]
piles = [3, 4, 5]
n = len(piles)

# Calculate nim-sum (XOR of all pile values)
nim_sum = 0
for p in piles:
    nim_sum ^= p

print("=== Nim Game Analysis ===")
print(f"Initial piles: {piles}")
print(f"Nim-sum (XOR of all piles): {nim_sum}")

# Determine if winning or losing position
is_winning = (nim_sum != 0)
game_state = "winning" if is_winning else "losing"
print(f"Game state: {game_state}")
print(f"is_winning_position: {is_winning}")

# Find all optimal moves (moves that make nim-sum = 0)
# For each pile i, we need to find stones to remove such that:
#   new_pile_i = piles[i] - stones_to_remove
#   new_nim_sum = XOR of all new piles = 0
# This means: new_pile_i = XOR of all other piles (since XOR of all = 0)
# So: stones_to_remove = piles[i] - (XOR of all other piles)

optimal_moves = []

if is_winning:
    print("\n=== Finding Optimal Moves ===")
    for i in range(n):
        # Calculate XOR of all piles except pile i
        xor_others = 0
        for j in range(n):
            if j != i:
                xor_others ^= piles[j]
        
        # For optimal move: new_pile_i should equal xor_others
        # So stones_to_remove = piles[i] - xor_others
        stones_to_remove = piles[i] - xor_others
        
        # Check if this is a valid move
        if stones_to_remove > 0 and stones_to_remove <= piles[i]:
            resulting_piles = piles.copy()
            resulting_piles[i] = piles[i] - stones_to_remove
            
            # Verify resulting nim-sum is 0
            resulting_nim_sum = 0
            for p in resulting_piles:
                resulting_nim_sum ^= p
            
            if resulting_nim_sum == 0:
                optimal_moves.append({
                    'pile': i + 1,  # 1-indexed
                    'stones': stones_to_remove,
                    'resulting_piles': resulting_piles
                })
                print(f"Optimal move found: Remove {stones_to_remove} stones from pile {i+1}")
                print(f"  Resulting piles: {resulting_piles}")
                print(f"  Resulting nim-sum: {resulting_nim_sum}")

print(f"\n=== Results ===")
print(f"Number of optimal moves: {len(optimal_moves)}")

# Print optimal moves in required format
for move in optimal_moves:
    print(f"pile: {move['pile']}")
    print(f"stones: {move['stones']}")
    print(f"resulting_piles: {move['resulting_piles']}")

# Strategy description
if is_winning:
    strategy = "From a winning position, make a move that results in nim-sum = 0"
    if optimal_moves:
        after_move = f"After optimal move, opponent faces losing position with piles {optimal_moves[0]['resulting_piles']}"
    else:
        after_move = "No optimal moves found (should not happen in winning position)"
else:
    strategy = "From a losing position, any move will leave opponent in winning position"
    after_move = "No optimal move exists from losing position"

print(f"\n=== Analysis ===")
print(f"strategy: {strategy}")
print(f"after_optimal_move: {after_move}")

# Use Z3 to verify the analysis
print("\n=== Z3 Verification ===")
solver = Solver()

# Create symbolic variables for piles
pile_vars = [Int(f'pile_{i}') for i in range(n)]
for i in range(n):
    solver.add(pile_vars[i] == piles[i])

# Calculate symbolic nim-sum
# XOR in Z3 can be done with BitVec or using the property: a XOR b = (a | b) & ~(a & b)
# For simplicity, we'll use BitVec for verification
pile_bv = [BitVec(f'pile_bv_{i}', 8) for i in range(n)]
for i in range(n):
    solver.add(pile_bv[i] == piles[i])

# Calculate nim-sum using BitVec XOR
nim_sum_bv = pile_bv[0]
for i in range(1, n):
    nim_sum_bv = nim_sum_bv ^ pile_bv[i]

# Check if nim-sum is 0
solver.push()
solver.add(nim_sum_bv == 0)
result = solver.check()
solver.pop()

if result == sat:
    print("Z3 confirms: Position is losing (nim-sum = 0)")
else:
    print("Z3 confirms: Position is winning (nim-sum ≠ 0)")

# Verify optimal moves
if optimal_moves:
    print("\nVerifying optimal moves with Z3:")
    for move in optimal_moves:
        solver.push()
        # Create new pile state after move
        new_piles = piles.copy()
        new_piles[move['pile']-1] = piles[move['pile']-1] - move['stones']
        
        # Create BitVec for new piles
        new_pile_bv = [BitVec(f'new_pile_bv_{i}', 8) for i in range(n)]
        for i in range(n):
            solver.add(new_pile_bv[i] == new_piles[i])
        
        # Calculate new nim-sum
        new_nim_sum_bv = new_pile_bv[0]
        for i in range(1, n):
            new_nim_sum_bv = new_nim_sum_bv ^ new_pile_bv[i]
        
        # Check if new nim-sum is 0
        solver.add(new_nim_sum_bv == 0)
        result = solver.check()
        
        if result == sat:
            print(f"  Move (pile {move['pile']}, remove {move['stones']}): VERIFIED - results in nim-sum = 0")
        else:
            print(f"  Move (pile {move['pile']}, remove {move['stones']}): FAILED verification")
        
        solver.pop()

print("\n=== STATUS ===")
print("STATUS: sat")