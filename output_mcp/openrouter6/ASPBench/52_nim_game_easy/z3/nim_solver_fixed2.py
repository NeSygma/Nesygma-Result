from z3 import *

# Instance data
initial_piles = [3, 4, 5]
current_player = "Player 1"

# Declare piles as BitVec (8 bits enough for small numbers)
piles = [BitVec(f'pile_{i}', 8) for i in range(3)]
solver = Solver()
for i in range(3):
    solver.add(piles[i] == initial_piles[i])

# Compute nim-sum using bitwise XOR
nim_sum_bv = piles[0] ^ piles[1] ^ piles[2]

# Check satisfiability (should be sat)
result = solver.check()
if result == sat:
    model = solver.model()
    # Evaluate nim-sum as integer
    nim_sum_val = model.eval(nim_sum_bv, model_completion=True).as_long()
    print(f"nim_sum = {nim_sum_val}")
    
    # Determine if winning position
    is_winning = nim_sum_val != 0
    game_state = "winning" if is_winning else "losing"
    print(f"game_state = {game_state}")
    print(f"is_winning_position = {is_winning}")
    
    # Find all optimal moves: moves that make nim-sum zero
    optimal_moves = []
    for pile_idx in range(3):
        pile_val = initial_piles[pile_idx]
        for stones_to_remove in range(1, pile_val + 1):
            new_piles = initial_piles.copy()
            new_piles[pile_idx] = pile_val - stones_to_remove
            new_nim_sum = new_piles[0] ^ new_piles[1] ^ new_piles[2]
            if new_nim_sum == 0:
                optimal_moves.append({
                    'pile': pile_idx + 1,  # 1-indexed
                    'stones': stones_to_remove,
                    'resulting_piles': new_piles
                })
    
    print(f"optimal_moves = {optimal_moves}")
    
    # Analysis
    analysis = {
        'is_winning_position': is_winning,
        'strategy': "From a winning position, make a move that results in nim-sum = 0.",
        'after_optimal_move': "After optimal move, opponent is in losing position (nim-sum = 0)."
    }
    print(f"analysis = {analysis}")
    
    # Print status
    print("STATUS: sat")
    # For multiple choice, we need to output answer: X
    # But this is not a multiple choice question; it's a model-finding puzzle.
    # However, the problem says "Expected optimal moves: 1 optimal move exists for this instance."
    # We can output the pile index of the optimal move as answer.
    if optimal_moves:
        print(f"answer:{optimal_moves[0]['pile']}")
    else:
        print("answer:none")
else:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")