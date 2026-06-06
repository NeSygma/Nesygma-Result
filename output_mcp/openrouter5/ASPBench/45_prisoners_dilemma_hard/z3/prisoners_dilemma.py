from z3 import *

# This is a deterministic calculation problem, not a constraint satisfaction problem.
# We can compute the expected scores directly using Python arithmetic.
# But since the instructions say to use Z3, we'll use Z3's Optimize to find the max.

# Define strategies
ego_strategies = ["COOP", "DEFECT", "TFT"]
opponent_types = ["type_A", "type_B", "type_C"]

# Opponent counts
opp_counts = {"type_A": 5, "type_B": 3, "type_C": 2}

# Payoff matrix for Ego (row: Ego move, col: Opponent move)
# payoff[ego_move][opp_move]
payoff = {
    ("C", "C"): 3,
    ("D", "C"): 5,
    ("C", "D"): 0,
    ("D", "D"): 1
}

# Define opponent strategies' moves for round 1 and round 2
# type_A: Always Defect -> (D, D)
# type_B: Tit-for-Tat -> round1: C, round2: copies Ego's round1 move
# type_C: Forgiving TFT -> round1: C, round2: C

# Ego strategies:
# COOP: (C, C)
# DEFECT: (D, D)
# TFT: round1: C, round2: copies opponent's round1 move

# We'll compute scores for each ego strategy against each opponent type
# using Z3 arithmetic to keep it symbolic, then maximize.

# Let's use Optimize to find which ego strategy gives max total score.

opt = Optimize()

# Decision variable: which ego strategy to pick (0=COOP, 1=DEFECT, 2=TFT)
choice = Int('choice')
opt.add(choice >= 0)
opt.add(choice <= 2)

# Total score variable
total_score = Int('total_score')

# We'll compute total score as sum over opponent types of (count * score_per_game)
# score_per_game = round1_score + round2_score

# For each ego strategy and opponent type, compute the score.
# We'll use If-then-else to encode the choice.

# Helper: given ego_move_r1, ego_move_r2, opp_move_r1, opp_move_r2, compute total score
def game_score(ego_r1, ego_r2, opp_r1, opp_r2):
    return payoff[(ego_r1, opp_r1)] + payoff[(ego_r2, opp_r2)]

# Precompute scores for each combination
# COOP vs type_A: ego=(C,C), opp=(D,D) -> 0+0=0
score_COOP_A = 0
# COOP vs type_B: ego=(C,C), opp=(C, C because opp copies ego r1 which is C) -> (C,C)=3, (C,C)=3 => 6
score_COOP_B = 6
# COOP vs type_C: ego=(C,C), opp=(C,C) -> 3+3=6
score_COOP_C = 6

# DEFECT vs type_A: ego=(D,D), opp=(D,D) -> 1+1=2
score_DEFECT_A = 2
# DEFECT vs type_B: ego=(D,D), opp=(C, D because opp copies ego r1 which is D) -> (D,C)=5, (D,D)=1 => 6
score_DEFECT_B = 6
# DEFECT vs type_C: ego=(D,D), opp=(C,C) -> (D,C)=5, (D,C)=5 => 10
score_DEFECT_C = 10

# TFT vs type_A: ego=(C, D because opp r1 is D), opp=(D,D) -> (C,D)=0, (D,D)=1 => 1
score_TFT_A = 1
# TFT vs type_B: ego=(C, C because opp r1 is C), opp=(C, C because opp copies ego r1 which is C) -> (C,C)=3, (C,C)=3 => 6
score_TFT_B = 6
# TFT vs type_C: ego=(C, C because opp r1 is C), opp=(C,C) -> (C,C)=3, (C,C)=3 => 6
score_TFT_C = 6

# Now compute total score based on choice
# total_score = sum over opponent types of count * score(choice, type)
total = (opp_counts["type_A"] * 
         If(choice == 0, score_COOP_A,
            If(choice == 1, score_DEFECT_A, score_TFT_A))) + \
        (opp_counts["type_B"] * 
         If(choice == 0, score_COOP_B,
            If(choice == 1, score_DEFECT_B, score_TFT_B))) + \
        (opp_counts["type_C"] * 
         If(choice == 0, score_COOP_C,
            If(choice == 1, score_DEFECT_C, score_TFT_C)))

opt.add(total_score == total)
opt.maximize(total_score)

result = opt.check()

if result == sat:
    m = opt.model()
    best_choice = m[choice].as_long()
    best_score = m[total_score].as_long()
    
    strategy_names = ["COOP", "DEFECT", "TFT"]
    best_strategy = strategy_names[best_choice]
    
    print("STATUS: sat")
    print(f"best_strategy_choice = {best_strategy}")
    print(f"expected_scores = [")
    
    # Compute scores for all strategies
    scores = []
    for idx, name in enumerate(strategy_names):
        s = (opp_counts["type_A"] * 
             (score_COOP_A if idx == 0 else (score_DEFECT_A if idx == 1 else score_TFT_A)) +
             opp_counts["type_B"] * 
             (score_COOP_B if idx == 0 else (score_DEFECT_B if idx == 1 else score_TFT_B)) +
             opp_counts["type_C"] * 
             (score_COOP_C if idx == 0 else (score_DEFECT_C if idx == 1 else score_TFT_C)))
        scores.append((name, s))
    
    # Sort descending by score
    scores.sort(key=lambda x: -x[1])
    for name, s in scores:
        print(f"  {{strategy: {name}, expected_total_score: {s}}}")
    print("]")
else:
    print("STATUS: unsat")