from z3 import *

# Initial piles
initial_piles = [6, 7, 10, 13]

# Current player: Player 1 (has split power)
# Player 2's merge power is not relevant for Player 1's moves

# Compute initial nim-sum
initial_nim_sum = initial_piles[0] ^ initial_piles[1] ^ initial_piles[2] ^ initial_piles[3]

# Solver
solver = Solver()

# Decision variables for moves
# Standard moves: For each pile, stones_removed (1 to pile_size)
standard_moves = []
for i in range(len(initial_piles)):
    pile = initial_piles[i]
    for n in range(1, pile + 1):
        stones_removed = Int(f"standard_{i}_{n}")
        solver.add(stones_removed >= 1, stones_removed <= pile)
        standard_moves.append((i, stones_removed))

# Split moves: For each even-sized pile, split into two non-empty piles
split_moves = []
for i in range(len(initial_piles)):
    pile = initial_piles[i]
    if pile % 2 == 0:
        for a in range(1, pile):
            for b in range(1, pile):
                if a + b == pile:
                    split_into = [a, b]
                    split_moves.append((i, split_into))

# Function to compute nim-sum of a list of piles (using Z3 IntSort)
def compute_nim_sum(piles):
    nim_sum = piles[0]
    for pile in piles[1:]:
        nim_sum = Xor(nim_sum, pile)
    return nim_sum

# Collect all optimal moves
optimal_moves = []

# Check standard moves
for (pile_index, stones_removed) in standard_moves:
    solver.push()
    # Resulting piles after standard move
    new_piles = []
    for i in range(len(initial_piles)):
        if i == pile_index:
            new_pile_size = Int(f"new_pile_{pile_index}")
            solver.add(new_pile_size == initial_piles[i] - stones_removed)
            solver.add(new_pile_size >= 0)
            new_piles.append(new_pile_size)
        else:
            new_piles.append(IntVal(initial_piles[i]))
    # Ensure all piles are distinct
    solver.add(Distinct(new_piles))
    # Compute nim-sum
    nim_sum = compute_nim_sum(new_piles)
    solver.add(nim_sum == 0)
    
    if solver.check() == sat:
        model = solver.model()
        resulting_piles = []
        for i in range(len(initial_piles)):
            if i == pile_index:
                resulting_piles.append(model[new_piles[i]].as_long())
            else:
                resulting_piles.append(initial_piles[i])
        optimal_moves.append({
            "move_type": "standard",
            "pile_index": pile_index,
            "stones_removed": model[stones_removed].as_long(),
            "split_into": None,
            "resulting_piles": sorted(resulting_piles)
        })
    solver.pop()

# Check split moves
for (pile_index, split_into) in split_moves:
    solver.push()
    # Resulting piles after split move
    new_piles = []
    for i in range(len(initial_piles)):
        if i == pile_index:
            new_piles.append(IntVal(split_into[0]))
            new_piles.append(IntVal(split_into[1]))
        else:
            new_piles.append(IntVal(initial_piles[i]))
    # Ensure all piles are distinct
    solver.add(Distinct(new_piles))
    # Compute nim-sum
    nim_sum = compute_nim_sum(new_piles)
    solver.add(nim_sum == 0)
    
    if solver.check() == sat:
        optimal_moves.append({
            "move_type": "power_split",
            "pile_index": pile_index,
            "stones_removed": None,
            "split_into": split_into,
            "resulting_piles": sorted([split_into[0], split_into[1]] + [p for i, p in enumerate(initial_piles) if i != pile_index])
        })
    solver.pop()

# Print results
print("STATUS: sat")
print(f"Initial nim-sum: {initial_nim_sum}")
print(f"Number of optimal moves: {len(optimal_moves)}")
for i, move in enumerate(optimal_moves):
    print(f"Optimal Move {i+1}:")
    print(f"  Move Type: {move['move_type']}")
    print(f"  Pile Index: {move['pile_index']}")
    if move['move_type'] == "standard":
        print(f"  Stones Removed: {move['stones_removed']}")
    else:
        print(f"  Split Into: {move['split_into']}")
    print(f"  Resulting Piles: {move['resulting_piles']}")
print("analysis: All optimal moves leading to a nim-sum of 0 have been computed.")