from z3 import *

# Let me re-examine the problem more carefully.
# The expected optimal score is 1218. Let me check if my simulation is correct.

# Let me trace through each match-up more carefully.

ROUNDS = 100

# Let's compute scores for each strategy playing against each opponent

def compute_match_score(stratA, stratB):
    """Compute exact or expected scores for a match."""
    
    # For deterministic strategies, simulate exactly
    # For probabilistic ones (RAND, GTFT), compute expected values
    
    # First, let's handle the deterministic cases
    
    # COOP always C
    # DEFECT always D
    # TFT: C first, then copy opponent's last move
    # GTFT: C first, then copy but forgive defection 10%
    # RAND: 50% C, 50% D
    
    # Let's simulate each match round by round for deterministic strategies
    
    def get_move_det(strat, opp_last_move, round_num):
        if strat == "COOP":
            return 'C'
        elif strat == "DEFECT":
            return 'D'
        elif strat == "TFT":
            if round_num == 0:
                return 'C'
            return opp_last_move
        elif strat == "GTFT":
            if round_num == 0:
                return 'C'
            # deterministic version: always retaliate (for non-probabilistic matchups)
            return opp_last_move
        return 'C'
    
    # For fully deterministic matchups, simulate
    deterministic_strats = {"COOP", "DEFECT", "TFT"}
    
    if stratA in deterministic_strats and stratB in deterministic_strats:
        scoreA, scoreB = 0, 0
        lastA, lastB = None, None
        for r in range(ROUNDS):
            mA = get_move_det(stratA, lastA, r)
            mB = get_move_det(stratB, lastB, r)
            if mA == 'C' and mB == 'C':
                scoreA += 3; scoreB += 3
            elif mA == 'D' and mB == 'D':
                scoreA += 1; scoreB += 1
            elif mA == 'C' and mB == 'D':
                scoreA += 0; scoreB += 5
            elif mA == 'D' and mB == 'C':
                scoreA += 5; scoreB += 0
            lastA, lastB = mB, mA
        return scoreA, scoreB
    
    return None, None  # needs expected value computation

# Let me compute all matchups systematically

print("=" * 60)
print("PRISONER'S DILEMMA TOURNAMENT - DETAILED ANALYSIS")
print("=" * 60)

# Each strategy plays against all 5 strategies (including itself)
# That's 5 opponents, each for 100 rounds
# Total rounds per strategy: 5 * 100 = 500

scores = {"COOP": 0, "DEFECT": 0, "TFT": 0, "GTFT": 0, "RAND": 0}

# --- COOP's matches ---

# COOP vs COOP: both always C -> (3,3) x 100
scores["COOP"] += 300  # self-play counts once? Or twice?
# In round-robin, each pair plays once. So COOP vs COOP is one match.
# COOP gets 300 from this match.
print(f"COOP vs COOP: COOP = 300")

# COOP vs DEFECT: COOP always C, DEFECT always D
# (C,D) -> (0,5) x 100
scores["COOP"] += 0
scores["DEFECT"] += 500
print(f"COOP vs DEFECT: COOP = 0, DEFECT = 500")

# COOP vs TFT: COOP always C, TFT plays C then copies
# Round 1: (C,C) -> (3,3)
# Round 2: COOP=C, TFT copies C -> (C,C) -> (3,3)
# ... all rounds: (3,3)
scores["COOP"] += 300
scores["TFT"] += 300
print(f"COOP vs TFT: COOP = 300, TFT = 300")

# COOP vs GTFT: COOP always C, GTFT plays C then copies (forgives but opponent never defects)
# Same as TFT: always (C,C) -> (3,3) x 100
scores["COOP"] += 300
scores["GTFT"] += 300
print(f"COOP vs GTFT: COOP = 300, GTFT = 300")

# COOP vs RAND: COOP always C, RAND 50/50
# Expected per round: COOP: 0.5*3 + 0.5*0 = 1.5, RAND: 0.5*3 + 0.5*5 = 4
scores["COOP"] += 150
scores["RAND"] += 400
print(f"COOP vs RAND: COOP = 150, RAND = 400")

print(f"  COOP subtotal: {scores['COOP']}")

# --- DEFECT's matches ---

# DEFECT vs DEFECT: both always D -> (1,1) x 100
scores["DEFECT"] += 100
print(f"DEFECT vs DEFECT: DEFECT = 100")

# DEFECT vs TFT: DEFECT always D, TFT plays C then copies
# Round 1: (D,C) -> (5,0)
# Round 2: DEFECT=D, TFT copies D -> (D,D) -> (1,1)
# Round 3-100: (D,D) -> (1,1) x 99
# DEFECT: 5 + 99*1 = 104
# TFT: 0 + 99*1 = 99
scores["DEFECT"] += 104
scores["TFT"] += 99
print(f"DEFECT vs TFT: DEFECT = 104, TFT = 99")

# DEFECT vs GTFT: DEFECT always D, GTFT plays C then copies with 10% forgiveness
# Round 1: (D,C) -> (5,0)
# Rounds 2-100: DEFECT=D, GTFT sees D
#   GTFT: 90% plays D, 10% plays C
#   Expected per round: 
#   90% (D,D) -> (1,1): DEFECT+1, GTFT+1
#   10% (D,C) -> (5,0): DEFECT+5, GTFT+0
#   DEFECT expected per round: 0.9*1 + 0.1*5 = 1.4
#   GTFT expected per round: 0.9*1 + 0.1*0 = 0.9
# DEFECT total: 5 + 99*1.4 = 5 + 138.6 = 143.6
# GTFT total: 0 + 99*0.9 = 89.1
scores["DEFECT"] += 143.6
scores["GTFT"] += 89.1
print(f"DEFECT vs GTFT: DEFECT = 143.6, GTFT = 89.1")

# DEFECT vs RAND: DEFECT always D, RAND 50/50
# Per round: 50% (D,C) -> (5,0), 50% (D,D) -> (1,1)
# DEFECT expected per round: 0.5*5 + 0.5*1 = 3
# RAND expected per round: 0.5*0 + 0.5*1 = 0.5
scores["DEFECT"] += 300
scores["RAND"] += 50
print(f"DEFECT vs RAND: DEFECT = 300, RAND = 50")

print(f"  DEFECT subtotal: {scores['DEFECT']}")

# --- TFT's matches ---

# TFT vs TFT: both play C then copy -> always (C,C) -> (3,3) x 100
scores["TFT"] += 300
print(f"TFT vs TFT: TFT = 300")

# TFT vs GTFT: both play C first, then copy each other
# Since GTFT only forgives when opponent defects, and TFT never defects against GTFT
# (both always C), this is always (C,C) -> (3,3) x 100
scores["TFT"] += 300
scores["GTFT"] += 300
print(f"TFT vs GTFT: TFT = 300, GTFT = 300")

# TFT vs RAND: TFT plays C then copies, RAND 50/50
# Round 1: TFT=C, RAND=50%C/50%D
#   If RAND=C: (3,3). TFT sees C -> next TFT=C
#   If RAND=D: (0,5). TFT sees D -> next TFT=D
#
# For rounds 2-100:
# TFT's move = RAND's previous move
# RAND is memoryless 50/50
# So P(TFT=C in round r) = P(RAND=C in round r-1) = 0.5 for r >= 2
# P(TFT=D in round r) = 0.5 for r >= 2
#
# Round 1 expected:
# TFT: 0.5*3 + 0.5*0 = 1.5
# RAND: 0.5*3 + 0.5*5 = 4
#
# Rounds 2-100 (99 rounds):
# When TFT=C (50%): RAND 50%C -> (3,3), 50%D -> (0,5)
#   TFT expected: 0.5*3 + 0.5*0 = 1.5
#   RAND expected: 0.5*3 + 0.5*5 = 4
# When TFT=D (50%): RAND 50%C -> (5,0), 50%D -> (1,1)
#   TFT expected: 0.5*5 + 0.5*1 = 3
#   RAND expected: 0.5*0 + 0.5*1 = 0.5
# Per round expected:
# TFT: 0.5*1.5 + 0.5*3 = 2.25
# RAND: 0.5*4 + 0.5*0.5 = 2.25
#
# TFT total: 1.5 + 99*2.25 = 1.5 + 222.75 = 224.25
# RAND total: 4 + 99*2.25 = 4 + 222.75 = 226.75
scores["TFT"] += 224.25
scores["RAND"] += 226.75
print(f"TFT vs RAND: TFT = 224.25, RAND = 226.75")

print(f"  TFT subtotal: {scores['TFT']}")

# --- GTFT's matches ---

# GTFT vs GTFT: both play C first, then copy
# Since neither defects (they only retaliate), always (C,C) -> (3,3) x 100
scores["GTFT"] += 300
print(f"GTFT vs GTFT: GTFT = 300")

# GTFT vs RAND: GTFT plays C then copies with 10% forgiveness, RAND 50/50
# Round 1: GTFT=C, RAND=50%C/50%D
#   If RAND=C (50%): (3,3). GTFT sees C -> next GTFT=C
#   If RAND=D (50%): (0,5). GTFT sees D -> 90% plays D, 10% plays C
#
# After round 1:
# P(GTFT=C in round 2) = P(RAND=C in round 1)*1 + P(RAND=D in round 1)*0.1
#                       = 0.5*1 + 0.5*0.1 = 0.55
# P(GTFT=D in round 2) = 0.45
#
# For rounds 2-100, this is a Markov chain.
# State: what GTFT plays (depends on RAND's previous move)
# P(GTFT=C in round r) = P(RAND=C in round r-1)*1 + P(RAND=D in round r-1)*0.1
#                       = 0.5*1 + 0.5*0.1 = 0.55 (steady state)
# So P(GTFT=C) = 0.55, P(GTFT=D) = 0.45 for rounds 2-100
#
# Round 1 expected:
# GTFT: 0.5*3 + 0.5*0 = 1.5
# RAND: 0.5*3 + 0.5*5 = 4
#
# Rounds 2-100 (99 rounds):
# GTFT=C (55%): RAND 50%C -> (3,3), 50%D -> (0,5)
#   GTFT: 0.5*3 + 0.5*0 = 1.5
#   RAND: 0.5*3 + 0.5*5 = 4
# GTFT=D (45%): RAND 50%C -> (5,0), 50%D -> (1,1)
#   GTFT: 0.5*5 + 0.5*1 = 3
#   RAND: 0.5*0 + 0.5*1 = 0.5
# Per round expected:
# GTFT: 0.55*1.5 + 0.45*3 = 0.825 + 1.35 = 2.175
# RAND: 0.55*4 + 0.45*0.5 = 2.2 + 0.225 = 2.425
#
# GTFT total: 1.5 + 99*2.175 = 1.5 + 215.325 = 216.825
# RAND total: 4 + 99*2.425 = 4 + 240.075 = 244.075
scores["GTFT"] += 216.825
scores["RAND"] += 244.075
print(f"GTFT vs RAND: GTFT = 216.825, RAND = 244.075")

print(f"  GTFT subtotal: {scores['GTFT']}")

# --- RAND's matches ---

# RAND vs RAND: both 50/50 independent
# Per round expected per player:
# 25% (C,C): 3, 25% (C,D): 0, 25% (D,C): 5, 25% (D,D): 1
# Expected: 0.25*3 + 0.25*0 + 0.25*5 + 0.25*1 = 2.25
scores["RAND"] += 225
print(f"RAND vs RAND: RAND = 225")

print(f"  RAND subtotal: {scores['RAND']}")

print("\n" + "=" * 60)
print("FINAL SCORES")
print("=" * 60)

sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
for name, score in sorted_scores:
    print(f"  {name}: {score:.2f}")

winner = sorted_scores[0][0]
print(f"\nWinner: {winner} with {sorted_scores[0][1]:.2f} points")

# Let me double check by also computing total
total = sum(scores.values())
print(f"\nTotal sum of all scores: {total:.2f}")

# Each match contributes to 2 scores (one per player)
# Number of matches: C(5,2) + 5 = 10 + 5 = 15 (pairs + self-play)
# Actually in round-robin with self-play: each of 5 strategies plays 5 opponents
# Total matches = 5*5 = 25... no, each pair plays once.
# With self-play: 5 choose 2 + 5 = 10 + 5 = 15 matches
# Each match has 100 rounds
# Total round-points: 15 * 100 = 1500 rounds
# Each round distributes: 3+3=6 (CC), 1+1=2 (DD), 0+5=5 (CD or DC)
# So total points per match varies.

# Let me verify: the expected optimal score is 1218.
# My winner TFT has 1523.25 which is way above 1218.
# Something is wrong with my calculation.

# Wait - the expected optimal score of 1218 might be for a DIFFERENT setup.
# Let me re-read the problem.

# "Expected optimal score: 1218" - this might just be a hint/check value.
# Let me verify my calculations more carefully.

print("\n\n=== VERIFICATION ===")
print("Let me verify each match-up carefully.")

# Let me recompute with a clean approach
print("\n--- Clean recomputation ---")

def compute_expected(stratA, stratB):
    """Compute expected scores for a match between two strategies."""
    
    if stratA == "COOP" and stratB == "COOP":
        return (300, 300)
    
    if stratA == "COOP" and stratB == "DEFECT":
        return (0, 500)
    
    if stratA == "COOP" and stratB == "TFT":
        return (300, 300)
    
    if stratA == "COOP" and stratB == "GTFT":
        return (300, 300)
    
    if stratA == "COOP" and stratB == "RAND":
        # COOP always C, RAND 50/50
        return (150, 400)
    
    if stratA == "DEFECT" and stratB == "DEFECT":
        return (100, 100)
    
    if stratA == "DEFECT" and stratB == "TFT":
        return (104, 99)
    
    if stratA == "DEFECT" and stratB == "GTFT":
        # Round 1: (D,C) -> (5,0)
        # Rounds 2-100: DEFECT=D, GTFT sees D -> 90%D, 10%C
        # DEFECT: 5 + 99*(0.9*1 + 0.1*5) = 5 + 99*1.4 = 143.6
        # GTFT: 0 + 99*(0.9*1 + 0.1*0) = 89.1
        return (143.6, 89.1)
    
    if stratA == "DEFECT" and stratB == "RAND":
        # DEFECT always D, RAND 50/50
        # 50% (D,C): (5,0), 50% (D,D): (1,1)
        return (300, 50)
    
    if stratA == "TFT" and stratB == "TFT":
        return (300, 300)
    
    if stratA == "TFT" and stratB == "GTFT":
        return (300, 300)
    
    if stratA == "TFT" and stratB == "RAND":
        # Round 1: TFT=C, RAND 50/50
        # Rounds 2-100: TFT copies RAND's last move, RAND 50/50
        # TFT: 1.5 + 99*2.25 = 224.25
        # RAND: 4 + 99*2.25 = 226.75
        return (224.25, 226.75)
    
    if stratA == "GTFT" and stratB == "GTFT":
        return (300, 300)
    
    if stratA == "GTFT" and stratB == "RAND":
        # GTFT: 1.5 + 99*2.175 = 216.825
        # RAND: 4 + 99*2.425 = 244.075
        return (216.825, 244.075)
    
    if stratA == "RAND" and stratB == "RAND":
        return (225, 225)
    
    return (0, 0)

# Build all matchups
strategies = ["COOP", "DEFECT", "TFT", "GTFT", "RAND"]
scores2 = {s: 0 for s in strategies}

for i, s1 in enumerate(strategies):
    for j, s2 in enumerate(strategies):
        if i <= j:  # each pair once
            sc1, sc2 = compute_expected(s1, s2)
            scores2[s1] += sc1
            scores2[s2] += sc2
            print(f"{s1:8s} vs {s2:8s}: ({sc1:8.2f}, {sc2:8.2f})")

print("\n--- Final Scores (verified) ---")
sorted2 = sorted(scores2.items(), key=lambda x: x[1], reverse=True)
for name, score in sorted2:
    print(f"  {name}: {score:.2f}")

print(f"\nWinner: {sorted2[0][0]} with {sorted2[0][1]:.2f}")
print(f"Total: {sum(scores2.values()):.2f}")