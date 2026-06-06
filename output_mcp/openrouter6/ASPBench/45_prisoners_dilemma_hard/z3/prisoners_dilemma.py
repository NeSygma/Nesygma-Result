from z3 import *

# Define constants for moves
COOPERATE = True
DEFECT = False

# Payoff matrix function
def payoff(ego_move, opp_move):
    """Returns payoff for Ego given moves"""
    return If(And(ego_move == COOPERATE, opp_move == COOPERATE), 3,
           If(And(ego_move == COOPERATE, opp_move == DEFECT), 0,
              If(And(ego_move == DEFECT, opp_move == COOPERATE), 5, 1)))

# Opponent counts
count_A = 5
count_B = 3
count_C = 2

# Strategy names
strategies = ["COOP", "DEFECT", "TFT"]

# Compute scores for each strategy
scores = {}

for strategy in strategies:
    total_score = 0
    
    # For each opponent type
    for opp_type, count in [("A", count_A), ("B", count_B), ("C", count_C)]:
        # Round 1 moves
        if strategy == "COOP":
            ego_r1 = COOPERATE
        elif strategy == "DEFECT":
            ego_r1 = DEFECT
        else:  # TFT
            ego_r1 = COOPERATE  # TFT always cooperates in round 1
        
        if opp_type == "A":
            opp_r1 = DEFECT  # Always defects
        elif opp_type == "B":
            opp_r1 = COOPERATE  # Tit-for-Tat: plays C in round 1
        else:  # type_C
            opp_r1 = COOPERATE  # Forgiving Tit-for-Tat: plays C in round 1
        
        # Score for round 1
        score_r1 = payoff(ego_r1, opp_r1)
        
        # Round 2 moves
        if strategy == "COOP":
            ego_r2 = COOPERATE
        elif strategy == "DEFECT":
            ego_r2 = DEFECT
        else:  # TFT
            # TFT copies opponent's round 1 move
            ego_r2 = opp_r1
        
        if opp_type == "A":
            opp_r2 = DEFECT  # Always defects
        elif opp_type == "B":
            # Tit-for-Tat copies Ego's round 1 move
            opp_r2 = ego_r1
        else:  # type_C
            opp_r2 = COOPERATE  # Always cooperates in round 2
        
        # Score for round 2
        score_r2 = payoff(ego_r2, opp_r2)
        
        # Total score for this matchup (2 rounds)
        matchup_score = score_r1 + score_r2
        
        # Add to total score (weighted by count)
        total_score += matchup_score * count
    
    scores[strategy] = total_score

# Create solver to find maximum
solver = Solver()

# Variables for scores (as integers)
score_vars = {s: Int(f"score_{s}") for s in strategies}

# Add constraints that score variables equal computed scores
for s in strategies:
    solver.add(score_vars[s] == scores[s])

# Find maximum score
max_score = Int("max_score")
solver.add(max_score == Max([score_vars[s] for s in strategies]))

# Check and get results
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Get scores for each strategy
    strategy_scores = {}
    for s in strategies:
        score_val = model.eval(score_vars[s], model_completion=True)
        strategy_scores[s] = int(score_val.as_string())
    
    # Find best strategy
    best_strategy = max(strategy_scores, key=strategy_scores.get)
    best_score = strategy_scores[best_strategy]
    
    # Sort strategies by score descending
    sorted_strategies = sorted(strategy_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Output results
    print(f"best_strategy_choice: {best_strategy}")
    print("expected_scores: [")
    for s, score in sorted_strategies:
        print(f'  {{"strategy": "{s}", "expected_total_score": {score}}},')
    print("]")
    
    # Verify expected optimal
    if best_strategy == "DEFECT" and best_score == 48:
        print("Verification: Matches expected optimal (DEFECT, 48)")
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")