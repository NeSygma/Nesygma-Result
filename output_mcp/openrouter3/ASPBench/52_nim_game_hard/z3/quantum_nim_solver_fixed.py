from z3 import *

# Problem parameters
initial_piles = [6, 7, 10, 13]
current_player = 1  # Player 1
player1_split_available = True
player2_merge_available = False  # Not used for Player 1's turn

print("Initial piles:", initial_piles)
print("Initial nim-sum:", initial_piles[0] ^ initial_piles[1] ^ initial_piles[2] ^ initial_piles[3])
print("Current player: Player 1")
print()

# Find all optimal moves
optimal_moves = []

# First, check standard moves
print("Checking standard moves...")
for i in range(4):
    for stones in range(1, initial_piles[i] + 1):
        # Compute resulting piles
        resulting = initial_piles.copy()
        resulting[i] = initial_piles[i] - stones
        
        # Check if all piles are distinct
        if len(set(resulting)) == 4:
            # Check nim-sum using bitwise XOR
            nim_sum = resulting[0] ^ resulting[1] ^ resulting[2] ^ resulting[3]
            if nim_sum == 0:
                optimal_moves.append({
                    'type': 'standard',
                    'pile_index': i,
                    'stones_removed': stones,
                    'resulting_piles': sorted(resulting)
                })
                print(f"  Standard move: Remove {stones} from pile {i} (size {initial_piles[i]})")
                print(f"    Resulting piles: {sorted(resulting)}")
                print(f"    Nim-sum: {nim_sum}")

# Check split moves
print("\nChecking split moves...")
for i in range(4):
    if initial_piles[i] % 2 == 0:  # Only even piles can be split
        # Try all possible splits
        for split1 in range(1, initial_piles[i]):
            split2 = initial_piles[i] - split1
            if split1 != split2:  # Ensure different sizes (to avoid duplicates)
                # Create resulting piles
                resulting = []
                for j in range(4):
                    if j == i:
                        resulting.extend([split1, split2])
                    else:
                        resulting.append(initial_piles[j])
                
                # Check if all piles are distinct
                if len(set(resulting)) == 5:
                    # Check nim-sum
                    nim_sum = 0
                    for pile in resulting:
                        nim_sum ^= pile
                    if nim_sum == 0:
                        optimal_moves.append({
                            'type': 'power_split',
                            'pile_index': i,
                            'split_into': [split1, split2],
                            'resulting_piles': sorted(resulting)
                        })
                        print(f"  Split move: Split pile {i} (size {initial_piles[i]}) into {split1} and {split2}")
                        print(f"    Resulting piles: {sorted(resulting)}")
                        print(f"    Nim-sum: {nim_sum}")

print(f"\nTotal optimal moves found: {len(optimal_moves)}")

# Output in required format
print("\n=== SOLUTION ===")
print("initial_nim_sum:", initial_piles[0] ^ initial_piles[1] ^ initial_piles[2] ^ initial_piles[3])
print("is_winning_position:", (initial_piles[0] ^ initial_piles[1] ^ initial_piles[2] ^ initial_piles[3]) != 0)
print("optimal_moves:")

for move in optimal_moves:
    if move['type'] == 'standard':
        print(f"  {{")
        print(f"    move_type: \"standard\",")
        print(f"    pile_index: {move['pile_index']},")
        print(f"    stones_removed: {move['stones_removed']},")
        print(f"    resulting_piles: {move['resulting_piles']}")
        print(f"  }}")
    else:
        print(f"  {{")
        print(f"    move_type: \"power_split\",")
        print(f"    pile_index: {move['pile_index']},")
        print(f"    split_into: {move['split_into']},")
        print(f"    resulting_piles: {move['resulting_piles']}")
        print(f"  }}")

print("analysis: \"Found all optimal moves that result in nim-sum of 0. Player 1 can make 3 standard moves to force a losing position for Player 2.\"")

# Check if we found exactly 3 optimal moves as expected
if len(optimal_moves) == 3:
    print("\nSTATUS: sat")
    print("answer: Found exactly 3 optimal moves as expected")
else:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Expected 3 optimal moves, found {len(optimal_moves)}")