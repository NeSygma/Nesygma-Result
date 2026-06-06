from z3 import *

# Payoff matrix (Ego's score)
def payoff(ego_move, opp_move):
    if ego_move == 'C':
        if opp_move == 'C':
            return 3
        else:  # opp_move == 'D'
            return 0
    else:  # ego_move == 'D'
        if opp_move == 'C':
            return 5
        else:  # opp_move == 'D'
            return 1

# Ego's strategies
def ego_COOP(round_num):
    return 'C'

def ego_DEFECT(round_num):
    return 'D'

def ego_TFT(opp_round1_move, round_num):
    if round_num == 1:
        return 'C'
    else:
        return opp_round1_move  # Copy opponent's move from round 1

# Opponent strategies
def opp_type_A(round_num):
    return 'D'  # Always Defect

def opp_type_B(ego_round1_move, round_num):
    if round_num == 1:
        return 'C'  # Cooperate in round 1
    else:
        return ego_round1_move  # Copy Ego's move from round 1

def opp_type_C(round_num):
    return 'C'  # Always Cooperate (Forgiving Tit-for-Tat)

# Compute score for a specific matchup
def compute_matchup_score(ego_strat, opp_strat):
    # Round 1
    if ego_strat.__name__ == "ego_TFT":
        ego_move1 = ego_strat(None, 1)  # TFT doesn't need opp_round1_move in round 1
    else:
        ego_move1 = ego_strat(1)
    
    if opp_strat.__name__ == "opp_type_B":
        opp_move1 = opp_strat(ego_move1, 1)
    else:
        opp_move1 = opp_strat(1)
    
    score1 = payoff(ego_move1, opp_move1)
    
    # Round 2
    if ego_strat.__name__ == "ego_TFT":
        ego_move2 = ego_strat(opp_move1, 2)
    else:
        ego_move2 = ego_strat(2)
    
    if opp_strat.__name__ == "opp_type_B":
        opp_move2 = opp_strat(ego_move1, 2)
    else:
        opp_move2 = opp_strat(2)
    
    score2 = payoff(ego_move2, opp_move2)
    
    return score1 + score2

# Opponent counts
counts = {"type_A": 5, "type_B": 3, "type_C": 2}

# Compute total expected scores for each of Ego's strategies
scores = {}
for strat_name in ["COOP", "DEFECT", "TFT"]:
    total_score = 0
    for opp_type in ["type_A", "type_B", "type_C"]:
        ego_func = globals()[f"ego_{strat_name}"]
        opp_func = globals()[f"opp_{opp_type}"]
        matchup_score = compute_matchup_score(ego_func, opp_func)
        total_score += matchup_score * counts[opp_type]
    scores[strat_name] = total_score

# Use Z3 to find the best strategy
opt = Optimize()

# Create variables for scores
score_vars = {name: Int(f"score_{name}") for name in scores}
for name, val in scores.items():
    opt.add(score_vars[name] == val)

# Find the maximum score
max_score = Int("max_score")
opt.add(max_score == Max([score_vars[name] for name in scores]))
opt.maximize(max_score)

# Check and print results
result = opt.check()
if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Determine the best strategy
    max_val = model.eval(max_score)
    best_strategy = None
    for name in ["COOP", "DEFECT", "TFT"]:
        if model.eval(score_vars[name]) == max_val:
            best_strategy = name
            break
    
    # Prepare expected_scores array
    expected_scores = [
        {"strategy": name, "expected_total_score": int(str(model.eval(score_vars[name])))}
        for name in ["COOP", "DEFECT", "TFT"]
    ]
    # Sort by score descending
    expected_scores.sort(key=lambda x: x["expected_total_score"], reverse=True)
    
    print(f"best_strategy_choice: {best_strategy}")
    print("expected_scores:")
    for item in expected_scores:
        print(f"  - strategy: {item['strategy']}")
        print(f"    expected_total_score: {item['expected_total_score']}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")