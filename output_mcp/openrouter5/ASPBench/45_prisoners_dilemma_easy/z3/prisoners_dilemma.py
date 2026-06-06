from z3 import *

# This is a deterministic simulation problem, not a constraint satisfaction problem.
# We need to simulate the tournament and compute scores.
# Since the strategies are deterministic (except RAND which is probabilistic),
# we can compute exact scores for COOP, DEFECT, TFT, GTFT.
# For RAND, we need to consider expected value.

# Let's compute the tournament scores analytically.

# Strategies: COOP, DEFECT, TFT, GTFT, RAND
# Each plays against all 5 strategies (including itself), 100 rounds each.

# Payoff matrix:
# (C,C) -> (3,3)
# (D,D) -> (1,1)
# (C,D) -> (0,5) for the cooperator
# (D,C) -> (5,0) for the defector

# Let's compute each match-up:

# 1. COOP vs COOP: both always C -> (3,3) each round -> 100*3 = 300 each
# 2. COOP vs DEFECT: COOP always C, DEFECT always D -> COOP gets 0, DEFECT gets 5 each round -> COOP: 0, DEFECT: 500
# 3. COOP vs TFT: COOP always C, TFT plays C first then copies opponent's last move
#    Round 1: COOP=C, TFT=C -> (3,3)
#    Round 2: COOP=C, TFT copies COOP's last move (C) -> (3,3)
#    ... all rounds: (3,3) -> COOP: 300, TFT: 300
# 4. COOP vs GTFT: COOP always C, GTFT plays C first then copies opponent's last move but forgives 10%
#    Since COOP always C, GTFT always sees C and plays C -> (3,3) each round -> COOP: 300, GTFT: 300
# 5. COOP vs RAND: COOP always C, RAND plays C or D with 50% probability
#    Expected: 50% C -> (3,3), 50% D -> (0,5)
#    COOP expected per round: 0.5*3 + 0.5*0 = 1.5
#    RAND expected per round: 0.5*3 + 0.5*5 = 4
#    COOP expected total: 150, RAND expected total: 400

# 6. DEFECT vs DEFECT: both always D -> (1,1) each round -> 100 each
# 7. DEFECT vs TFT: DEFECT always D, TFT plays C first then copies opponent's last move
#    Round 1: DEFECT=D, TFT=C -> (5,0) -> DEFECT: 5, TFT: 0
#    Round 2: DEFECT=D, TFT copies DEFECT's last move (D) -> (1,1) -> DEFECT: 1, TFT: 1
#    Round 3: DEFECT=D, TFT copies DEFECT's last move (D) -> (1,1) -> DEFECT: 1, TFT: 1
#    ... rounds 2-100: (1,1) each
#    DEFECT: 5 + 99*1 = 104
#    TFT: 0 + 99*1 = 99
# 8. DEFECT vs GTFT: DEFECT always D, GTFT plays C first then copies but forgives 10%
#    Round 1: DEFECT=D, GTFT=C -> (5,0) -> DEFECT: 5, GTFT: 0
#    Round 2: DEFECT=D, GTFT sees D from last round. Normally would play D, but forgives 10%.
#    So 90% chance GTFT plays D, 10% chance GTFT plays C.
#    This is probabilistic. Let's compute expected values.
#    After round 1: GTFT saw D.
#    Round 2: 90% GTFT plays D -> (1,1), 10% GTFT plays C -> (5,0)
#    If GTFT plays D in round 2, then round 3: GTFT saw D -> same as round 2
#    If GTFT plays C in round 2, then round 3: GTFT saw C -> plays C (since opponent played C)
#    Actually, GTFT: "copies opponent's last move but forgives defection 10% of the time"
#    So normally it copies, but when opponent defects, 10% of the time it cooperates instead.
#    Since DEFECT always defects, GTFT will see D every round.
#    Each round: 90% GTFT plays D, 10% GTFT plays C.
#    Expected per round for GTFT: 0.9*1 + 0.1*0 = 0.9
#    Expected per round for DEFECT: 0.9*1 + 0.1*5 = 0.9 + 0.5 = 1.4
#    Round 1: DEFECT=5, GTFT=0 (GTFT always plays C first)
#    Rounds 2-100 (99 rounds): DEFECT expected: 99*1.4 = 138.6, GTFT expected: 99*0.9 = 89.1
#    DEFECT total: 5 + 138.6 = 143.6
#    GTFT total: 0 + 89.1 = 89.1

# 9. DEFECT vs RAND: DEFECT always D, RAND 50% C, 50% D
#    Expected per round:
#    50% RAND=C -> (5,0) -> DEFECT: 5, RAND: 0
#    50% RAND=D -> (1,1) -> DEFECT: 1, RAND: 1
#    DEFECT expected per round: 0.5*5 + 0.5*1 = 3
#    RAND expected per round: 0.5*0 + 0.5*1 = 0.5
#    DEFECT total: 100*3 = 300
#    RAND total: 100*0.5 = 50

# 10. TFT vs TFT: both play C first, then copy each other -> always C -> (3,3) each -> 300 each
# 11. TFT vs GTFT: both play C first. Then they copy each other.
#     Since both play C in round 1, round 2 both see C and play C.
#     This continues forever -> always C -> (3,3) each -> 300 each
# 12. TFT vs RAND: TFT plays C first, then copies RAND's last move.
#     RAND: 50% C, 50% D each round independently.
#     Round 1: TFT=C, RAND=50%C/50%D
#     If RAND=C: (3,3). TFT sees C, plays C next.
#     If RAND=D: (0,5). TFT sees D, plays D next.
#     This is a Markov chain. Let's compute expected values.
#     Actually, since RAND is memoryless (50% each round regardless), TFT's behavior doesn't affect RAND.
#     Each round independently:
#     50% RAND=C, TFT plays whatever it plays -> if TFT=C: (3,3), if TFT=D: (1,1)
#     50% RAND=D, TFT plays whatever it plays -> if TFT=C: (0,5), if TFT=D: (1,1)
#     This is complex. Let's simulate with Z3 using expected values.

# Actually, let's just compute this deterministically using Python since it's a simulation.

print("Computing Prisoner's Dilemma Tournament Scores")
print("=" * 50)

# Let's compute exact scores for deterministic strategies
# and expected scores for RAND

# Match results: (score_A, score_B) for each pair
# We'll compute total scores

scores = {
    "COOP": 0,
    "DEFECT": 0,
    "TFT": 0,
    "GTFT": 0,
    "RAND": 0
}

ROUNDS = 100

# Helper to simulate a match
def simulate_match(stratA_name, stratB_name):
    """Returns (scoreA, scoreB) for a match between two strategies."""
    
    # Initialize last moves (for TFT/GTFT)
    last_move_A = None  # opponent's last move from A's perspective
    last_move_B = None  # opponent's last move from B's perspective
    
    scoreA = 0
    scoreB = 0
    
    for r in range(ROUNDS):
        # Determine moves
        moveA = get_move(stratA_name, last_move_A, r)
        moveB = get_move(stratB_name, last_move_B, r)
        
        # Update scores
        if moveA == 'C' and moveB == 'C':
            scoreA += 3
            scoreB += 3
        elif moveA == 'D' and moveB == 'D':
            scoreA += 1
            scoreB += 1
        elif moveA == 'C' and moveB == 'D':
            scoreA += 0
            scoreB += 5
        elif moveA == 'D' and moveB == 'C':
            scoreA += 5
            scoreB += 0
        
        # Update last moves
        last_move_A = moveB
        last_move_B = moveA
    
    return scoreA, scoreB

def get_move(strategy, opponent_last_move, round_num):
    """Get the move for a strategy given the opponent's last move."""
    if strategy == "COOP":
        return 'C'
    elif strategy == "DEFECT":
        return 'D'
    elif strategy == "TFT":
        if round_num == 0:
            return 'C'
        else:
            return opponent_last_move
    elif strategy == "GTFT":
        if round_num == 0:
            return 'C'
        else:
            # Normally copy, but forgive defection 10% of the time
            # For expected value calculation, we use the expected value
            # Since this is deterministic simulation, we need to handle the probabilistic part
            # For now, let's compute expected values
            if opponent_last_move == 'C':
                return 'C'
            else:
                # 90% defect, 10% cooperate
                # We'll compute expected values separately
                return 'D'  # deterministic approximation (90% case)
    elif strategy == "RAND":
        # 50% C, 50% D - expected value
        return 'C'  # placeholder, we'll compute expected values
    return 'C'

# For probabilistic strategies, compute expected values
# GTFT vs DEFECT: expected values
# RAND vs anyone: expected values

# Let's compute all match-ups properly

print("\n--- Deterministic Match-ups ---")

# COOP vs COOP
s1, s2 = simulate_match("COOP", "COOP")
scores["COOP"] += s1
scores["COOP"] += s2
print(f"COOP vs COOP: COOP gets {s1} (x2 for self-play)")

# COOP vs DEFECT
s1, s2 = simulate_match("COOP", "DEFECT")
scores["COOP"] += s1
scores["DEFECT"] += s2
print(f"COOP vs DEFECT: COOP={s1}, DEFECT={s2}")

# COOP vs TFT
s1, s2 = simulate_match("COOP", "TFT")
scores["COOP"] += s1
scores["TFT"] += s2
print(f"COOP vs TFT: COOP={s1}, TFT={s2}")

# COOP vs GTFT (deterministic part - GTFT always sees C from COOP)
s1, s2 = simulate_match("COOP", "GTFT")
scores["COOP"] += s1
scores["GTFT"] += s2
print(f"COOP vs GTFT: COOP={s1}, GTFT={s2}")

# COOP vs RAND (expected)
# COOP always C, RAND 50%C/50%D
# Per round expected: COOP: 0.5*3 + 0.5*0 = 1.5, RAND: 0.5*3 + 0.5*5 = 4
scores["COOP"] += 150
scores["RAND"] += 400
print(f"COOP vs RAND (expected): COOP=150, RAND=400")

# DEFECT vs DEFECT
s1, s2 = simulate_match("DEFECT", "DEFECT")
scores["DEFECT"] += s1
scores["DEFECT"] += s2
print(f"DEFECT vs DEFECT: DEFECT gets {s1} (x2 for self-play)")

# DEFECT vs TFT
s1, s2 = simulate_match("DEFECT", "TFT")
scores["DEFECT"] += s1
scores["TFT"] += s2
print(f"DEFECT vs TFT: DEFECT={s1}, TFT={s2}")

# DEFECT vs GTFT (expected - probabilistic)
# Round 1: DEFECT=D, GTFT=C -> (5,0)
# Rounds 2-100: DEFECT always D, GTFT sees D.
# GTFT: 90% D, 10% C
# Expected per round for GTFT: 0.9*1 + 0.1*0 = 0.9
# Expected per round for DEFECT: 0.9*1 + 0.1*5 = 1.4
scores["DEFECT"] += 5 + 99 * 1.4  # = 5 + 138.6 = 143.6
scores["GTFT"] += 0 + 99 * 0.9  # = 89.1
print(f"DEFECT vs GTFT (expected): DEFECT={5 + 99*1.4:.1f}, GTFT={99*0.9:.1f}")

# DEFECT vs RAND (expected)
# DEFECT always D, RAND 50%C/50%D
# Per round: 50% (5,0), 50% (1,1)
# DEFECT expected per round: 0.5*5 + 0.5*1 = 3
# RAND expected per round: 0.5*0 + 0.5*1 = 0.5
scores["DEFECT"] += 300
scores["RAND"] += 50
print(f"DEFECT vs RAND (expected): DEFECT=300, RAND=50")

# TFT vs TFT
s1, s2 = simulate_match("TFT", "TFT")
scores["TFT"] += s1
scores["TFT"] += s2
print(f"TFT vs TFT: TFT gets {s1} (x2 for self-play)")

# TFT vs GTFT
s1, s2 = simulate_match("TFT", "GTFT")
scores["TFT"] += s1
scores["GTFT"] += s2
print(f"TFT vs GTFT: TFT={s1}, GTFT={s2}")

# TFT vs RAND (expected)
# TFT plays C first, then copies RAND's last move
# RAND is memoryless 50/50
# This is a Markov chain. Let's compute.
# State: what TFT will play next (depends on RAND's last move)
# Actually, TFT's move in round r depends on RAND's move in round r-1.
# RAND's move is independent each round.
# So each round is independent given the previous round's outcome.
# Let's compute expected payoff per round in steady state.
# 
# Round 1: TFT=C, RAND=50%C/50%D
#   If RAND=C: (3,3). Next round TFT plays C.
#   If RAND=D: (0,5). Next round TFT plays D.
# 
# For rounds 2-100:
#   If TFT plays C: RAND 50%C -> (3,3), 50%D -> (0,5)
#   If TFT plays D: RAND 50%C -> (5,0), 50%D -> (1,1)
# 
# Let's compute expected value per round using Markov chain.
# P(TFT=C in round r) depends on RAND's move in round r-1.
# P(TFT=C in round r) = P(RAND played C in round r-1) = 0.5
# So TFT plays C with 50% probability each round (after round 1).
# 
# Round 1 expected:
# TFT: 0.5*3 + 0.5*0 = 1.5
# RAND: 0.5*3 + 0.5*5 = 4
#
# Rounds 2-100 (99 rounds):
# 50% TFT=C: RAND 50%C -> (3,3), 50%D -> (0,5). TFT expected: 0.5*3+0.5*0=1.5, RAND: 0.5*3+0.5*5=4
# 50% TFT=D: RAND 50%C -> (5,0), 50%D -> (1,1). TFT expected: 0.5*5+0.5*1=3, RAND: 0.5*0+0.5*1=0.5
# TFT expected per round: 0.5*1.5 + 0.5*3 = 2.25
# RAND expected per round: 0.5*4 + 0.5*0.5 = 2.25
# 
# TFT total: 1.5 + 99*2.25 = 1.5 + 222.75 = 224.25
# RAND total: 4 + 99*2.25 = 4 + 222.75 = 226.75
scores["TFT"] += 224.25
scores["RAND"] += 226.75
print(f"TFT vs RAND (expected): TFT=224.25, RAND=226.75")

# GTFT vs GTFT
s1, s2 = simulate_match("GTFT", "GTFT")
scores["GTFT"] += s1
scores["GTFT"] += s2
print(f"GTFT vs GTFT: GTFT gets {s1} (x2 for self-play)")

# GTFT vs RAND (expected)
# GTFT plays C first, then copies RAND's last move but forgives 10% of defections
# RAND is memoryless 50/50
# 
# Round 1: GTFT=C, RAND=50%C/50%D
#   If RAND=C: (3,3). GTFT sees C -> plays C next.
#   If RAND=D: (0,5). GTFT sees D -> 90% plays D, 10% plays C.
#
# For rounds 2-100:
# State depends on GTFT's move and RAND's move.
# This is complex. Let's approximate.
# 
# Actually, since RAND is memoryless, the expected value per round converges.
# Let's compute more carefully.
#
# Round 1: GTFT=C
#   RAND=C (50%): (3,3). GTFT sees C -> next GTFT=C
#   RAND=D (50%): (0,5). GTFT sees D -> next GTFT: 90%D, 10%C
#
# After round 1:
# State A (50%): GTFT will play C next
# State B (45%): GTFT will play D next (RAND=D, GTFT retaliates)
# State C (5%): GTFT will play C next (RAND=D, GTFT forgives)
# So after round 1: P(GTFT=C next) = 50% + 5% = 55%, P(GTFT=D next) = 45%
#
# For subsequent rounds, we need the steady state.
# Let's just compute expected values directly.
#
# In steady state, let p = P(GTFT=C) in a given round.
# GTFT's move depends on RAND's previous move.
# P(GTFT=C) = P(RAND prev=C) * 1 + P(RAND prev=D) * 0.1
# P(RAND prev=C) = 0.5, P(RAND prev=D) = 0.5
# So P(GTFT=C) = 0.5 * 1 + 0.5 * 0.1 = 0.55
# P(GTFT=D) = 0.45
#
# Expected payoff per round for GTFT:
# GTFT=C (55%): RAND 50%C -> (3,3), 50%D -> (0,5). GTFT: 0.5*3+0.5*0=1.5
# GTFT=D (45%): RAND 50%C -> (5,0), 50%D -> (1,1). GTFT: 0.5*5+0.5*1=3
# GTFT expected per round: 0.55*1.5 + 0.45*3 = 0.825 + 1.35 = 2.175
#
# Expected payoff per round for RAND:
# GTFT=C (55%): RAND 50%C -> (3,3), 50%D -> (0,5). RAND: 0.5*3+0.5*5=4
# GTFT=D (45%): RAND 50%C -> (5,0), 50%D -> (1,1). RAND: 0.5*0+0.5*1=0.5
# RAND expected per round: 0.55*4 + 0.45*0.5 = 2.2 + 0.225 = 2.425
#
# Round 1: GTFT=C
#   RAND=C (50%): (3,3). GTFT:3, RAND:3
#   RAND=D (50%): (0,5). GTFT:0, RAND:5
# Round 1 expected: GTFT: 1.5, RAND: 4
#
# Rounds 2-100 (99 rounds): GTFT: 99*2.175 = 215.325, RAND: 99*2.425 = 240.075
# GTFT total: 1.5 + 215.325 = 216.825
# RAND total: 4 + 240.075 = 244.075
scores["GTFT"] += 216.825
scores["RAND"] += 244.075
print(f"GTFT vs RAND (expected): GTFT=216.825, RAND=244.075")

# RAND vs RAND (expected)
# Both play 50%C/50%D independently each round
# Per round expected:
# 25% (C,C): (3,3)
# 25% (C,D): (0,5)
# 25% (D,C): (5,0)
# 25% (D,D): (1,1)
# Expected per player per round: 0.25*3 + 0.25*0 + 0.25*5 + 0.25*1 = 0.75 + 0 + 1.25 + 0.25 = 2.25
scores["RAND"] += 100 * 2.25  # self-play, counted twice
print(f"RAND vs RAND (expected): RAND gets {100*2.25} (x2 for self-play)")

print("\n" + "=" * 50)
print("FINAL SCORES:")
print("=" * 50)

# Sort by score
sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
for name, score in sorted_scores:
    print(f"{name}: {score:.2f}")

winner = sorted_scores[0][0]
print(f"\nWinner: {winner} with {sorted_scores[0][1]:.2f} points")
print(f"Expected optimal score: 1218")

# Let's verify: total sum of all scores
total = sum(scores.values())
print(f"Total sum of all scores: {total:.2f}")