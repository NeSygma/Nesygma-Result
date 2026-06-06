from z3 import *

# We'll compute scores for each (ego_strategy, opponent_type) pair by modeling
# the 2-round game explicitly, then weight by opponent counts.

# Define moves as: 0 = C, 1 = D
C, D = 0, 1

# Payoff matrix for Ego: (ego_move, opp_move) -> score
def ego_payoff(ego_move, opp_move):
    # CC=3, DC=5, CD=0, DD=1
    return If(And(ego_move == C, opp_move == C), 3,
           If(And(ego_move == D, opp_move == C), 5,
           If(And(ego_move == C, opp_move == D), 0,
           If(And(ego_move == D, opp_move == D), 1, 0))))

# For each ego strategy and opponent type, compute the 2-round game score
# We'll use Z3 to model each game and extract concrete scores

solver = Solver()

# We'll create symbolic games for each (ego_strategy, opponent_type) pair
# and compute scores. Since strategies are deterministic, we can model them.

# Game variables: ego_r1, ego_r2, opp_r1, opp_r2 for each matchup
# Ego strategies: COOP, DEFECT, TFT
# Opponent types: type_A, type_B, type_C

# We'll compute scores for all 9 matchups

matchups = {}

for ego_strat in ["COOP", "DEFECT", "TFT"]:
    for opp_type in ["type_A", "type_B", "type_C"]:
        prefix = f"{ego_strat}_vs_{opp_type}"
        
        ego_r1 = Int(f'{prefix}_ego_r1')
        ego_r2 = Int(f'{prefix}_ego_r2')
        opp_r1 = Int(f'{prefix}_opp_r1')
        opp_r2 = Int(f'{prefix}_opp_r2')
        
        # Domain: 0 (C) or 1 (D)
        for v in [ego_r1, ego_r2, opp_r1, opp_r2]:
            solver.add(Or(v == C, v == D))
        
        # Ego strategy constraints
        if ego_strat == "COOP":
            solver.add(ego_r1 == C)
            solver.add(ego_r2 == C)
        elif ego_strat == "DEFECT":
            solver.add(ego_r1 == D)
            solver.add(ego_r2 == D)
        elif ego_strat == "TFT":
            solver.add(ego_r1 == C)
            # Round 2: copy opponent's round 1
            solver.add(ego_r2 == opp_r1)
        
        # Opponent strategy constraints
        if opp_type == "type_A":
            solver.add(opp_r1 == D)
            solver.add(opp_r2 == D)
        elif opp_type == "type_B":
            solver.add(opp_r1 == C)
            # Round 2: copy Ego's round 1
            solver.add(opp_r2 == ego_r1)
        elif opp_type == "type_C":
            solver.add(opp_r1 == C)
            solver.add(opp_r2 == C)
        
        # Compute score for this matchup
        score = ego_payoff(ego_r1, opp_r1) + ego_payoff(ego_r2, opp_r2)
        matchups[(ego_strat, opp_type)] = score

# Opponent counts
opp_counts = {"type_A": 5, "type_B": 3, "type_C": 2}

# Compute total expected score for each ego strategy
total_scores = {}
for ego_strat in ["COOP", "DEFECT", "TFT"]:
    total = Sum([matchups[(ego_strat, opp_type)] * opp_counts[opp_type] 
                 for opp_type in ["type_A", "type_B", "type_C"]])
    total_scores[ego_strat] = total

# Now find which strategy maximizes total score
# We'll check each strategy and see which gives the highest score

# First, let's get the actual scores by checking satisfiability
result = solver.check()
if result == sat:
    m = solver.model()
    
    # Extract scores for each strategy
    strategy_scores = {}
    for ego_strat in ["COOP", "DEFECT", "TFT"]:
        total = 0
        for opp_type in ["type_A", "type_B", "type_C"]:
            score_val = m.evaluate(matchups[(ego_strat, opp_type)])
            count = opp_counts[opp_type]
            total += score_val.as_long() * count
        strategy_scores[ego_strat] = total
    
    print("STATUS: sat")
    print("Strategy scores:")
    for s, sc in sorted(strategy_scores.items(), key=lambda x: -x[1]):
        print(f"  {s}: {sc}")
    
    best = max(strategy_scores, key=strategy_scores.get)
    print(f"best_strategy_choice: {best}")
    print(f"expected_scores (descending):")
    for s, sc in sorted(strategy_scores.items(), key=lambda x: -x[1]):
        print(f"  {{strategy: {s}, expected_total_score: {sc}}}")
else:
    print("STATUS: unsat")
    print("Could not solve the game model")