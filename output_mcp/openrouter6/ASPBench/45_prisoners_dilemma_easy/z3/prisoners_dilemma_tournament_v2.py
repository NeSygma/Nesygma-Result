from z3 import *

# Strategy indices
COOP, DEFECT, TFT, GTFT, RAND = 0, 1, 2, 3, 4
strategies = [COOP, DEFECT, TFT, GTFT, RAND]
strategy_names = ["COOP", "DEFECT", "TFT", "GTFT", "RAND"]

# Create solver
solver = Solver()

# Total scores for each strategy
score = [Int(f'score_{i}') for i in range(5)]
for s in score:
    solver.add(s >= 0)

# We'll accumulate scores by adding match payoffs
# Initialize scores to 0
for i in range(5):
    solver.add(score[i] == 0)

# Helper to get move for a strategy given round, opponent's last move, and random variable
def get_move(strategy, round_idx, opponent_last_move, random_var):
    """Return Z3 expression for move (True = cooperate, False = defect)."""
    if strategy == COOP:
        return True
    elif strategy == DEFECT:
        return False
    elif strategy == TFT:
        if round_idx == 0:
            return True
        else:
            return opponent_last_move
    elif strategy == GTFT:
        if round_idx == 0:
            return True
        else:
            # If opponent defected last round, use random_var (forgive with prob 0.1)
            # else cooperate (copy opponent's last move which is True)
            return If(opponent_last_move == False, random_var, True)
    elif strategy == RAND:
        return random_var
    else:
        raise ValueError("Unknown strategy")

# Iterate over all matches (including self)
for i in range(5):
    for j in range(i, 5):  # include self, and each pair once
        # For this match, we simulate 100 rounds
        # We'll store move variables for each round for both players
        move_i = [Bool(f'move_i_{i}_{j}_r{r}') for r in range(100)]
        move_j = [Bool(f'move_j_{i}_{j}_r{r}') for r in range(100)]
        
        # Random variables for GTFT and RAND
        # For each round, we may need random variables for each player if they are GTFT or RAND
        random_i = [Bool(f'rand_i_{i}_{j}_r{r}') for r in range(100)]
        random_j = [Bool(f'rand_j_{i}_{j}_r{r}') for r in range(100)]
        
        # For each round, define moves based on strategy types
        for r in range(100):
            # opponent's last move (for round 0, we define a dummy value, but it's not used)
            opp_last_i = True if r == 0 else move_j[r-1]
            opp_last_j = True if r == 0 else move_i[r-1]
            
            # Get move expressions
            move_i_expr = get_move(strategies[i], r, opp_last_i, random_i[r])
            move_j_expr = get_move(strategies[j], r, opp_last_j, random_j[r])
            
            # Add constraints to enforce the moves
            solver.add(move_i[r] == move_i_expr)
            solver.add(move_j[r] == move_j_expr)
        
        # Compute total payoff for this match for each player
        total_payoff_i = Int(f'total_payoff_i_{i}_{j}')
        total_payoff_j = Int(f'total_payoff_j_{i}_{j}')
        solver.add(total_payoff_i >= 0)
        solver.add(total_payoff_j >= 0)
        
        # Sum of payoffs over rounds
        sum_i = Sum([If(And(move_i[r], move_j[r]), 3,
                        If(And(Not(move_i[r]), Not(move_j[r])), 1,
                            If(move_i[r], 0, 5))) for r in range(100)])
        sum_j = Sum([If(And(move_j[r], move_i[r]), 3,
                        If(And(Not(move_j[r]), Not(move_i[r])), 1,
                            If(move_j[r], 0, 5))) for r in range(100)])
        
        solver.add(total_payoff_i == sum_i)
        solver.add(total_payoff_j == sum_j)
        
        # Add to overall scores
        solver.add(score[i] == score[i] + total_payoff_i)
        if i != j:
            solver.add(score[j] == score[j] + total_payoff_j)

# Now we have the model. We want to find the maximum possible total score for each strategy.
# We'll use Optimize for each strategy separately.
print("Building model done. Now optimizing for each strategy...")

max_scores = []
for idx in range(5):
    opt = Optimize()
    # Add all constraints from solver to opt
    for c in solver.assertions():
        opt.add(c)
    # Maximize score[idx]
    h = opt.maximize(score[idx])
    result = opt.check()
    if result == sat:
        model = opt.model()
        max_score = model[score[idx]]
        max_scores.append(max_score)
        print(f"Strategy {strategy_names[idx]} max possible score: {max_score}")
    else:
        print(f"Strategy {strategy_names[idx]} optimization result: {result}")
        max_scores.append(None)

# Determine winner (highest max score)
winner_idx = None
winner_score = None
for idx, ms in enumerate(max_scores):
    if ms is not None:
        if winner_score is None or ms > winner_score:
            winner_score = ms
            winner_idx = idx

if winner_idx is not None:
    print(f"\nWinner: {strategy_names[winner_idx]} with max possible score {winner_score}")
    print("STATUS: sat")
    print(f"answer:{strategy_names[winner_idx]}")
else:
    print("STATUS: unsat")
    print("Refine: No strategy found")