from z3 import *

# ============================================================
# Prisoners' Dilemma Tournament - Z3 Model
# ============================================================

solver = Optimize()

# --- Constants ---
ROUNDS = 2
NUM_STRATEGIES = 3  # COOP=0, DEFECT=1, TFT=2
NUM_OPP_TYPES = 3   # type_A=0, type_B=1, type_C=2

# Opponent counts
opp_counts = [5, 3, 2]  # type_A=5, type_B=3, type_C=2

# Payoff matrix for Ego: (ego_move, opp_move) -> points
# C=0, D=1
payoff = {(0,0): 3, (1,0): 5, (0,1): 0, (1,1): 1}

# --- Decision Variable ---
# ego_strat: 0=COOP, 1=DEFECT, 2=TFT
ego_strat = Int('ego_strat')
solver.add(ego_strat >= 0, ego_strat <= 2)

# --- Model the game rounds symbolically ---
# For each opponent type (0,1,2) and each round (0,1), determine moves
# ego_move[opp_type][round], opp_move[opp_type][round]
ego_move = [[Int(f'ego_m_{o}_{r}') for r in range(ROUNDS)] for o in range(NUM_OPP_TYPES)]
opp_move = [[Int(f'opp_m_{o}_{r}') for r in range(ROUNDS)] for o in range(NUM_OPP_TYPES)]

# Moves are binary: 0=Cooperate, 1=Defect
for o in range(NUM_OPP_TYPES):
    for r in range(ROUNDS):
        solver.add(Or(ego_move[o][r] == 0, ego_move[o][r] == 1))
        solver.add(Or(opp_move[o][r] == 0, opp_move[o][r] == 1))

# --- Ego Strategy Constraints ---
for o in range(NUM_OPP_TYPES):
    # COOP: always cooperate
    solver.add(Implies(ego_strat == 0, And(ego_move[o][0] == 0, ego_move[o][1] == 0)))
    # DEFECT: always defect
    solver.add(Implies(ego_strat == 1, And(ego_move[o][0] == 1, ego_move[o][1] == 1)))
    # TFT: cooperate round 1, copy opponent's previous move in round 2
    solver.add(Implies(ego_strat == 2, And(ego_move[o][0] == 0, ego_move[o][1] == opp_move[o][0])))

# --- Opponent Strategy Constraints ---
for o in range(NUM_OPP_TYPES):
    # type_A (o=0): always defect
    solver.add(Implies(o == 0, And(opp_move[o][0] == 1, opp_move[o][1] == 1)))
    # type_B (o=1): TFT - cooperate round 1, copy Ego's previous move
    solver.add(Implies(o == 1, And(opp_move[o][0] == 0, opp_move[o][1] == ego_move[o][0])))
    # type_C (o=2): always cooperate
    solver.add(Implies(o == 2, And(opp_move[o][0] == 0, opp_move[o][1] == 0)))

# --- Score Calculation ---
# Score for each opponent type = sum of payoffs over 2 rounds
scores = [Int(f'score_{o}') for o in range(NUM_OPP_TYPES)]
for o in range(NUM_OPP_TYPES):
    # Build payoff expressions for each round
    round_payoffs = []
    for r in range(ROUNDS):
        # payoff[ego_move, opp_move] using nested If
        # If ego=C(0): If opp=C(0) -> 3, else -> 0
        # If ego=D(1): If opp=C(0) -> 5, else -> 1
        rp = If(ego_move[o][r] == 0,
                If(opp_move[o][r] == 0, 3, 0),
                If(opp_move[o][r] == 0, 5, 1))
        round_payoffs.append(rp)
    solver.add(scores[o] == Sum(round_payoffs))

# Total expected score = sum of (score * opponent_count) for each opponent type
total_score = Int('total_score')
solver.add(total_score == Sum([scores[o] * opp_counts[o] for o in range(NUM_OPP_TYPES)]))

# --- Maximize total score ---
solver.maximize(total_score)

# --- Solve ---
BENCHMARK_MODE = True
result = solver.check()

if result == sat:
    m = solver.model()
    strat_val = m[ego_strat].as_long()
    strat_names = {0: "COOP", 1: "DEFECT", 2: "TFT"}
    best = strat_names[strat_val]
    total = m[total_score].as_long()
    
    # Compute scores for ALL strategies for the expected_scores array
    # We'll enumerate each strategy
    all_scores = []
    for s in range(NUM_STRATEGIES):
        s_solver = Solver()
        s_ego_strat = Int('ego_strat')
        s_solver.add(s_ego_strat == s)
        
        s_ego_move = [[Int(f'ego_m_{o}_{r}') for r in range(ROUNDS)] for o in range(NUM_OPP_TYPES)]
        s_opp_move = [[Int(f'opp_m_{o}_{r}') for r in range(ROUNDS)] for o in range(NUM_OPP_TYPES)]
        
        for o in range(NUM_OPP_TYPES):
            for r in range(ROUNDS):
                s_solver.add(Or(s_ego_move[o][r] == 0, s_ego_move[o][r] == 1))
                s_solver.add(Or(s_opp_move[o][r] == 0, s_opp_move[o][r] == 1))
        
        for o in range(NUM_OPP_TYPES):
            s_solver.add(Implies(s == 0, And(s_ego_move[o][0] == 0, s_ego_move[o][1] == 0)))
            s_solver.add(Implies(s == 1, And(s_ego_move[o][0] == 1, s_ego_move[o][1] == 1)))
            s_solver.add(Implies(s == 2, And(s_ego_move[o][0] == 0, s_ego_move[o][1] == s_opp_move[o][0])))
        
        for o in range(NUM_OPP_TYPES):
            s_solver.add(Implies(o == 0, And(s_opp_move[o][0] == 1, s_opp_move[o][1] == 1)))
            s_solver.add(Implies(o == 1, And(s_opp_move[o][0] == 0, s_opp_move[o][1] == s_ego_move[o][0])))
            s_solver.add(Implies(o == 2, And(s_opp_move[o][0] == 0, s_opp_move[o][1] == 0)))
        
        s_scores = [Int(f'score_{o}') for o in range(NUM_OPP_TYPES)]
        for o in range(NUM_OPP_TYPES):
            round_payoffs = []
            for r in range(ROUNDS):
                rp = If(s_ego_move[o][r] == 0,
                        If(s_opp_move[o][r] == 0, 3, 0),
                        If(s_opp_move[o][r] == 0, 5, 1))
                round_payoffs.append(rp)
            s_solver.add(s_scores[o] == Sum(round_payoffs))
        
        s_total = Int('total_score')
        s_solver.add(s_total == Sum([s_scores[o] * opp_counts[o] for o in range(NUM_OPP_TYPES)]))
        
        if s_solver.check() == sat:
            sm = s_solver.model()
            all_scores.append({
                "strategy": strat_names[s],
                "expected_total_score": sm[s_total].as_long()
            })
    
    # Sort descending by score
    all_scores.sort(key=lambda x: x["expected_total_score"], reverse=True)
    
    print("STATUS: sat")
    print(f"best_strategy_choice: {best}")
    print(f"expected_total_score: {total}")
    print("expected_scores:")
    for entry in all_scores:
        print(f"  {entry['strategy']}: {entry['expected_total_score']}")
    print(f"answer:{best}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")