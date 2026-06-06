from z3 import *

def solve_nim_game():
    # Initial piles
    initial_piles = [3, 4, 5]
    
    # Create solver
    solver = Solver()
    
    # Declare symbolic variables for piles after move
    piles = [Int(f'pile_{i}') for i in range(3)]
    
    # Declare move variables
    pile_index = Int('pile_index')  # 0, 1, 2 (0-indexed)
    stones_removed = Int('stones_removed')
    
    # Current piles before move (constant)
    current_piles = [IntVal(3), IntVal(4), IntVal(5)]
    
    # Constraint: pile_index must be 0, 1, or 2
    solver.add(Or(pile_index == 0, pile_index == 1, pile_index == 2))
    
    # Constraint: stones_removed must be at least 1
    solver.add(stones_removed >= 1)
    
    # Constraint: stones_removed cannot exceed current pile value
    # Use Or-Loop pattern to avoid indexing with Z3 variable
    for i in range(3):
        solver.add(Or(
            pile_index != i,
            stones_removed <= current_piles[i]
        ))
    
    # Constraint: exactly one pile changes, others stay the same
    for i in range(3):
        solver.add(Or(
            pile_index != i,
            piles[i] == current_piles[i] - stones_removed
        ))
        solver.add(Or(
            pile_index == i,
            piles[i] == current_piles[i]
        ))
    
    # Calculate nim-sum (XOR of all piles)
    # Z3 doesn't have direct XOR for integers, so we use bitwise XOR
    nim_sum = piles[0] ^ piles[1] ^ piles[2]
    
    # Constraint: resulting nim-sum must be 0 (optimal move)
    solver.add(nim_sum == 0)
    
    # Check for solutions
    print("=== Nim Game Analysis ===")
    print(f"Initial piles: {initial_piles}")
    print(f"Current player: Player 1")
    
    # Calculate current nim-sum
    current_nim_sum = initial_piles[0] ^ initial_piles[1] ^ initial_piles[2]
    print(f"Current nim-sum: {current_nim_sum}")
    
    is_winning = current_nim_sum != 0
    game_state = "winning" if is_winning else "losing"
    print(f"Game state: {game_state}")
    
    # Find all optimal moves
    optimal_moves = []
    move_count = 0
    
    while solver.check() == sat:
        move_count += 1
        model = solver.model()
        
        # Extract move details
        pile_idx = model[pile_index].as_long()
        stones = model[stones_removed].as_long()
        
        # Calculate resulting piles
        resulting_piles = list(initial_piles)
        resulting_piles[pile_idx] -= stones
        
        # Store move (convert to 1-indexed for output)
        move = {
            'pile': pile_idx + 1,  # 1-indexed
            'stones': stones,
            'resulting_piles': resulting_piles
        }
        optimal_moves.append(move)
        
        # Block this specific solution to find next one
        # Add constraint that at least one variable must differ
        solver.add(Or(
            pile_index != model[pile_index],
            stones_removed != model[stones_removed]
        ))
    
    # Output results
    print(f"\n=== Results ===")
    print(f"Number of optimal moves found: {len(optimal_moves)}")
    
    if optimal_moves:
        print("\nOptimal moves:")
        for i, move in enumerate(optimal_moves, 1):
            print(f"  Move {i}: Remove {move['stones']} stones from pile {move['pile']}")
            print(f"    Resulting piles: {move['resulting_piles']}")
            print(f"    Nim-sum after move: {move['resulting_piles'][0] ^ move['resulting_piles'][1] ^ move['resulting_piles'][2]}")
    
    # Game-theoretic analysis
    print(f"\n=== Analysis ===")
    print(f"is_winning_position: {is_winning}")
    
    if is_winning:
        print("strategy: From a winning position, make a move that results in nim-sum = 0")
        if optimal_moves:
            print(f"after_optimal_move: Position becomes losing (nim-sum = 0)")
        else:
            print("after_optimal_move: No optimal moves found (unexpected)")
    else:
        print("strategy: From a losing position, any move leads to a winning position for opponent")
        print("after_optimal_move: Position becomes winning for opponent")
    
    # Print final status
    if optimal_moves:
        print(f"\nSTATUS: sat")
        print(f"answer:{optimal_moves[0]['pile']}")  # First optimal move
    else:
        print(f"\nSTATUS: unsat")
        print("Refine: No optimal moves found")

if __name__ == "__main__":
    solve_nim_game()