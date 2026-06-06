from z3 import *

def solve_quantum_nim():
    # Current game state
    piles = [6, 7, 10, 13]
    initial_nim_sum = 6  # XOR of all piles
    is_winning_position = initial_nim_sum != 0
    
    optimal_moves = []
    
    # 1. Find optimal standard moves
    print("Finding optimal standard moves...")
    for i in range(4):  # pile index
        for N in range(1, piles[i] + 1):  # stones to remove
            # Create new piles after move
            new_piles = piles.copy()
            new_piles[i] = piles[i] - N
            
            # Check distinctness
            if len(set(new_piles)) != 4:
                continue
                
            # Compute nim-sum
            nim = 0
            for p in new_piles:
                nim ^= p
                
            if nim == 0:
                # This is an optimal move
                move = {
                    "move_type": "standard",
                    "pile_index": i,
                    "stones_removed": N,
                    "resulting_piles": sorted(new_piles)
                }
                optimal_moves.append(move)
                print(f"Found standard move: pile {i}, remove {N} stones")
    
    # 2. Find optimal split moves
    print("\nFinding optimal split moves...")
    for i in range(4):  # pile index
        if piles[i] % 2 == 0:  # only even piles can be split
            # Try all possible splits
            for a in range(1, piles[i]):
                b = piles[i] - a
                if a >= b:  # avoid duplicates and ensure a < b
                    continue
                if a == b:  # must be distinct
                    continue
                    
                # Create new piles after split
                new_piles = piles.copy()
                # Remove the original pile and add the two new piles
                new_piles.pop(i)
                new_piles.extend([a, b])
                
                # Check distinctness
                if len(set(new_piles)) != 5:
                    continue
                    
                # Compute nim-sum
                nim = 0
                for p in new_piles:
                    nim ^= p
                    
                if nim == 0:
                    # This is an optimal move
                    move = {
                        "move_type": "power_split",
                        "pile_index": i,
                        "split_into": [a, b],
                        "resulting_piles": sorted(new_piles)
                    }
                    optimal_moves.append(move)
                    print(f"Found split move: pile {i}, split into {a} and {b}")
    
    # Output results
    print("\n" + "="*50)
    print("RESULTS:")
    print(f"initial_nim_sum: {initial_nim_sum}")
    print(f"is_winning_position: {is_winning_position}")
    print(f"optimal_moves: {optimal_moves}")
    
    # Analysis
    analysis = f"Initial nim-sum is {initial_nim_sum}, which is non-zero, so this is a winning position for Player 1. "
    analysis += f"Found {len(optimal_moves)} optimal moves that result in nim-sum 0: "
    for idx, move in enumerate(optimal_moves):
        if move['move_type'] == 'standard':
            analysis += f"{idx+1}. Standard move on pile {move['pile_index']} removing {move['stones_removed']} stones. "
        else:
            analysis += f"{idx+1}. Split move on pile {move['pile_index']} into {move['split_into']}. "
    
    print(f"analysis: {analysis}")
    
    # Print status
    if len(optimal_moves) > 0:
        print("\nSTATUS: sat")
    else:
        print("\nSTATUS: unsat")
        if BENCHMARK_MODE:
            print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")

# Set benchmark mode
BENCHMARK_MODE = True

# Run the solver
solve_quantum_nim()