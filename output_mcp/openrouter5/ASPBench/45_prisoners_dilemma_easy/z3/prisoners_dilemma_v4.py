# Let me re-think this problem from scratch.
# The problem says "Expected optimal score: 1218"
# This is a specific number. Let me figure out what configuration gives 1218.

# Let me try: what if the tournament is structured so that each strategy
# plays against each OTHER strategy (not including itself), and the
# expected optimal score is 1218?

# Let me compute more carefully.

# Strategies: COOP, DEFECT, TFT, GTFT, RAND
# Each strategy plays against the other 4 strategies.
# 100 rounds per match.

# Let me compute the expected score for each strategy against each opponent.

# First, let me define the payoff matrix:
# (C, C) -> (3, 3)
# (D, D) -> (1, 1)
# (C, D) -> (0, 5)  [cooperator gets 0, defector gets 5]
# (D, C) -> (5, 0)  [defector gets 5, cooperator gets 0]

# COOP vs DEFECT:
# COOP always plays C, DEFECT always plays D.
# Round 1: COOP plays C, DEFECT plays D -> COOP gets 0, DEFECT gets 5
# Rounds 2-100: same -> COOP gets 0, DEFECT gets 5 each round
# COOP total: 0 * 100 = 0
# DEFECT total: 5 * 100 = 500

# COOP vs TFT:
# COOP always plays C.
# TFT plays C in round 1, then copies opponent's last move.
# Round 1: COOP plays C, TFT plays C -> both get 3
# Round 2: COOP plays C, TFT copies COOP's last move (C) -> both get 3
# ... all rounds: both get 3
# COOP total: 3 * 100 = 300
# TFT total: 3 * 100 = 300

# COOP vs GTFT:
# GTFT plays C in round 1, then copies opponent's last move but forgives 10%.
# Since COOP always plays C, GTFT always sees C and plays C.
# All rounds: both get 3
# COOP total: 3 * 100 = 300
# GTFT total: 3 * 100 = 300

# COOP vs RAND:
# COOP always plays C.
# RAND plays C or D with 50% probability.
# Expected: 50 rounds (C,C) -> 3 each, 50 rounds (C,D) -> COOP gets 0, RAND gets 5
# COOP expected: 50 * 3 + 50 * 0 = 150
# RAND expected: 50 * 3 + 50 * 5 = 400

# DEFECT vs TFT:
# DEFECT always plays D.
# TFT plays C in round 1, then copies opponent's last move.
# Round 1: DEFECT plays D, TFT plays C -> DEFECT gets 5, TFT gets 0
# Round 2: DEFECT plays D, TFT copies DEFECT's last move (D) -> both get 1
# Rounds 3-100: DEFECT plays D, TFT plays D -> both get 1
# DEFECT total: 5 + 99 * 1 = 104
# TFT total: 0 + 99 * 1 = 99

# DEFECT vs GTFT:
# DEFECT always plays D.
# GTFT plays C in round 1, then copies opponent's last move but forgives 10%.
# Round 1: DEFECT plays D, GTFT plays C -> DEFECT gets 5, GTFT gets 0
# Round 2: DEFECT plays D, GTFT sees D and would normally play D, but forgives 10%.
#   With 90% probability: GTFT plays D -> both get 1
#   With 10% probability: GTFT plays C -> DEFECT gets 5, GTFT gets 0
# This is complex. Let me think about it differently.

# GTFT: Like TFT but forgives defection 10% of the time.
# This means: normally GTFT copies opponent's last move (like TFT),
# but when the opponent defected, GTFT cooperates 10% of the time instead of defecting.

# So GTFT's behavior:
# - First move: C
# - If opponent's last move was C: play C
# - If opponent's last move was D: play D with 90% probability, C with 10% probability

# DEFECT vs GTFT:
# DEFECT always plays D.
# GTFT plays C in round 1.
# Round 1: DEFECT plays D, GTFT plays C -> DEFECT gets 5, GTFT gets 0
# Round 2: DEFECT plays D. GTFT sees D (opponent's last move).
#   With 90%: GTFT plays D -> both get 1
#   With 10%: GTFT plays C -> DEFECT gets 5, GTFT gets 0
# If GTFT plays D in round 2:
#   Round 3: DEFECT plays D. GTFT sees D.
#     With 90%: GTFT plays D -> both get 1
#     With 10%: GTFT plays C -> DEFECT gets 5, GTFT gets 0
# If GTFT plays C in round 2:
#   Round 3: DEFECT plays D. GTFT sees D (opponent's last move was D).
#     With 90%: GTFT plays D -> both get 1
#     With 10%: GTFT plays C -> DEFECT gets 5, GTFT gets 0

# So regardless of what GTFT does, DEFECT always plays D, and GTFT always sees D.
# Each round after round 1: GTFT plays D with 90%, C with 10%.
# DEFECT expected score per round (after round 1): 0.9 * 1 + 0.1 * 5 = 0.9 + 0.5 = 1.4
# GTFT expected score per round (after round 1): 0.9 * 1 + 0.1 * 0 = 0.9

# DEFECT total: 5 + 99 * 1.4 = 5 + 138.6 = 143.6
# GTFT total: 0 + 99 * 0.9 = 89.1

# DEFECT vs RAND:
# DEFECT always plays D.
# RAND plays C or D with 50% probability.
# Expected: 50 rounds (D,C) -> DEFECT gets 5, RAND gets 0
#           50 rounds (D,D) -> both get 1
# DEFECT expected: 50 * 5 + 50 * 1 = 300
# RAND expected: 50 * 0 + 50 * 1 = 50

# TFT vs GTFT:
# Both play C in round 1 -> both get 3
# Both see C and play C in round 2 -> both get 3
# ... all rounds: both get 3
# TFT total: 300
# GTFT total: 300

# TFT vs RAND:
# TFT plays C in round 1.
# RAND plays C or D with 50% probability.
# Round 1: TFT plays C. RAND plays C (50%) or D (50%).
#   If RAND plays C: both get 3. TFT sees C, plays C in round 2.
#   If RAND plays D: TFT gets 0, RAND gets 5. TFT sees D, plays D in round 2.
# This is a Markov chain. Let me compute the expected score.

# Actually, for TFT vs RAND, this is complex because TFT's move depends on RAND's last move.
# Let me think of it as a Markov chain with states based on TFT's move.

# State: TFT's move in the current round.
# TFT plays C in round 1.
# RAND plays C (50%) or D (50%).
# If RAND plays C: TFT plays C in next round. State: C.
# If RAND plays D: TFT plays D in next round. State: D.

# In state C (TFT plays C):
# RAND plays C (50%): both get 3. Next state: C.
# RAND plays D (50%): TFT gets 0, RAND gets 5. Next state: D.

# In state D (TFT plays D):
# RAND plays C (50%): TFT gets 5, RAND gets 0. Next state: C (TFT copies RAND's C).
# RAND plays D (50%): both get 1. Next state: D.

# This is a Markov chain with transition matrix:
# From C: to C with 50%, to D with 50%
# From D: to C with 50%, to D with 50%

# Stationary distribution: 50% C, 50% D.

# Expected score per round in state C: 0.5 * 3 + 0.5 * 0 = 1.5
# Expected score per round in state D: 0.5 * 5 + 0.5 * 1 = 3.0

# Expected score per round (stationary): 0.5 * 1.5 + 0.5 * 3.0 = 2.25

# TFT total (100 rounds): 100 * 2.25 = 225... wait, but round 1 is special.
# Round 1: TFT plays C. RAND plays C (50%) or D (50%).
# Expected round 1 score: 0.5 * 3 + 0.5 * 0 = 1.5
# Rounds 2-100 (99 rounds): expected score per round = 2.25
# TFT total: 1.5 + 99 * 2.25 = 1.5 + 222.75 = 224.25

# RAND expected score:
# Round 1: 0.5 * 3 + 0.5 * 5 = 4
# Rounds 2-100: 
#   In state C (TFT plays C): 0.5 * 3 + 0.5 * 5 = 4
#   In state D (TFT plays D): 0.5 * 0 + 0.5 * 1 = 0.5
#   Expected: 0.5 * 4 + 0.5 * 0.5 = 2.25
# RAND total: 4 + 99 * 2.25 = 4 + 222.75 = 226.75

# GTFT vs RAND:
# GTFT plays C in round 1.
# RAND plays C or D with 50% probability.
# Round 1: GTFT plays C. RAND plays C (50%) or D (50%).
#   If RAND plays C: both get 3. GTFT sees C, plays C in round 2.
#   If RAND plays D: GTFT gets 0, RAND gets 5. GTFT sees D.
#     GTFT forgives 10%: plays C with 10%, D with 90%.

# This is more complex. Let me model it as a Markov chain.

# State: (GTFT's move, RAND's move) or just GTFT's move since RAND is random.
# Actually, GTFT's move depends on RAND's last move.
# RAND's move is always random (50% C, 50% D), independent of history.

# So the state is just GTFT's move in the current round.
# GTFT plays C in round 1.

# In state C (GTFT plays C):
# RAND plays C (50%): both get 3. GTFT sees C. Next state: C.
# RAND plays D (50%): GTFT gets 0, RAND gets 5. GTFT sees D.
#   With 90%: GTFT plays D. Next state: D.
#   With 10%: GTFT plays C. Next state: C.

# In state D (GTFT plays D):
# RAND plays C (50%): GTFT gets 5, RAND gets 0. GTFT sees C. Next state: C.
# RAND plays D (50%): both get 1. GTFT sees D.
#   With 90%: GTFT plays D. Next state: D.
#   With 10%: GTFT plays C. Next state: C.

# Transition matrix:
# From C: to C with 0.5 + 0.5*0.1 = 0.55, to D with 0.5*0.9 = 0.45
# From D: to C with 0.5 + 0.5*0.1 = 0.55, to D with 0.5*0.9 = 0.45

# Stationary distribution: 55% C, 45% D.

# Expected score per round in state C: 0.5 * 3 + 0.5 * 0 = 1.5
# Expected score per round in state D: 0.5 * 5 + 0.5 * 1 = 3.0

# Expected score per round (stationary): 0.55 * 1.5 + 0.45 * 3.0 = 0.825 + 1.35 = 2.175

# GTFT total (100 rounds):
# Round 1: GTFT plays C. 0.5 * 3 + 0.5 * 0 = 1.5
# Rounds 2-100 (99 rounds): 99 * 2.175 = 215.325
# GTFT total: 1.5 + 215.325 = 216.825

# RAND expected score:
# Round 1: 0.5 * 3 + 0.5 * 5 = 4
# Rounds 2-100:
#   In state C (GTFT plays C): 0.5 * 3 + 0.5 * 5 = 4
#   In state D (GTFT plays D): 0.5 * 0 + 0.5 * 1 = 0.5
#   Expected: 0.55 * 4 + 0.45 * 0.5 = 2.2 + 0.225 = 2.425
# RAND total: 4 + 99 * 2.425 = 4 + 240.075 = 244.075

# RAND vs RAND:
# Both play C or D with 50% probability, independently.
# Expected: 25% (C,C): both get 3
#           25% (C,D): first gets 0, second gets 5
#           25% (D,C): first gets 5, second gets 0
#           25% (D,D): both get 1
# Expected score per round: 0.25 * 3 + 0.25 * 0 + 0.25 * 5 + 0.25 * 1 = 0.75 + 0 + 1.25 + 0.25 = 2.25
# RAND total (vs RAND): 100 * 2.25 = 225

# Now let me compute total scores for each strategy (with self-play):

# COOP:
# vs COOP: 300
# vs DEFECT: 0
# vs TFT: 300
# vs GTFT: 300
# vs RAND: 150
# Total: 300 + 0 + 300 + 300 + 150 = 1050

# DEFECT:
# vs COOP: 500
# vs DEFECT: 100
# vs TFT: 104
# vs GTFT: 143.6
# vs RAND: 300
# Total: 500 + 100 + 104 + 143.6 + 300 = 1147.6

# TFT:
# vs COOP: 300
# vs DEFECT: 99
# vs TFT: 300
# vs GTFT: 300
# vs RAND: 224.25
# Total: 300 + 99 + 300 + 300 + 224.25 = 1223.25

# GTFT:
# vs COOP: 300
# vs DEFECT: 89.1
# vs TFT: 300
# vs GTFT: 300
# vs RAND: 216.825
# Total: 300 + 89.1 + 300 + 300 + 216.825 = 1205.925

# RAND:
# vs COOP: 400
# vs DEFECT: 50
# vs TFT: 226.75
# vs GTFT: 244.075
# vs RAND: 225
# Total: 400 + 50 + 226.75 + 244.075 + 225 = 1145.825

# Hmm, TFT = 1223.25, GTFT = 1205.925
# The expected optimal score is 1218.
# 1223.25 is close to 1218 but not exact.
# 1205.925 is also close but not exact.

# Wait, let me re-check TFT vs RAND.
# Actually, I think my Markov chain analysis might be slightly off.
# Let me redo it more carefully.

# TFT vs RAND:
# Round 1: TFT plays C.
# RAND plays C (50%) or D (50%).

# If RAND plays C in round 1:
#   Round 1: (C,C) -> both get 3
#   TFT sees C, plays C in round 2.
#   This is state C.

# If RAND plays D in round 1:
#   Round 1: (C,D) -> TFT gets 0, RAND gets 5
#   TFT sees D, plays D in round 2.
#   This is state D.

# State C (TFT plays C):
# RAND plays C (50%): (C,C) -> both get 3. TFT sees C. Next state: C.
# RAND plays D (50%): (C,D) -> TFT gets 0, RAND gets 5. TFT sees D. Next state: D.

# State D (TFT plays D):
# RAND plays C (50%): (D,C) -> TFT gets 5, RAND gets 0. TFT sees C. Next state: C.
# RAND plays D (50%): (D,D) -> both get 1. TFT sees D. Next state: D.

# Transition matrix P:
# P(C->C) = 0.5, P(C->D) = 0.5
# P(D->C) = 0.5, P(D->D) = 0.5

# Stationary distribution: π(C) = 0.5, π(D) = 0.5

# Expected TFT score:
# In state C: E_C = 0.5 * 3 + 0.5 * 0 = 1.5
# In state D: E_D = 0.5 * 5 + 0.5 * 1 = 3.0

# Expected score per round (stationary): 0.5 * 1.5 + 0.5 * 3.0 = 2.25

# Round 1: TFT plays C. Expected score = 0.5 * 3 + 0.5 * 0 = 1.5
# Rounds 2-100: 99 * 2.25 = 222.75
# Total: 1.5 + 222.75 = 224.25

# This seems correct.

# Let me check: what if the expected optimal score of 1218 is for TFT
# but with a slightly different calculation?

# Actually, wait. Let me re-check TFT vs DEFECT.
# TFT plays C in round 1. DEFECT plays D.
# Round 1: (C,D) -> TFT gets 0, DEFECT gets 5.
# Round 2: TFT copies DEFECT's last move (D). DEFECT plays D.
# (D,D) -> both get 1.
# Rounds 3-100: same as round 2.
# TFT total: 0 + 99 * 1 = 99
# DEFECT total: 5 + 99 * 1 = 104

# This seems correct.

# Let me re-check TFT vs TFT (self-play):
# Both play C in round 1 -> both get 3.
# Both see C, play C in round 2 -> both get 3.
# ... all rounds: both get 3.
# TFT total: 300.

# This seems correct.

# TFT total: 300 + 99 + 300 + 300 + 224.25 = 1223.25

# Hmm, 1223.25 is close to 1218 but not exact.
# The difference is 5.25.

# Let me check if maybe the expected optimal score is for GTFT.
# GTFT total: 300 + 89.1 + 300 + 300 + 216.825 = 1205.925
# Difference from 1218: 12.075.

# Let me check if maybe the expected optimal score is for a tournament
# WITHOUT self-play.

# TFT (without self-play): 300 + 99 + 300 + 224.25 = 923.25
# GTFT (without self-play): 300 + 89.1 + 300 + 216.825 = 905.925
# DEFECT (without self-play): 500 + 104 + 143.6 + 300 = 1047.6

# None of these are 1218.

# Let me try: what if the expected optimal score is for a tournament
# where each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for... let me check if maybe
# I made an error in my calculations.

# Actually, let me try a completely different approach.
# What if the expected optimal score of 1218 is for a tournament where
# each strategy plays against each OTHER strategy (not including itself),
# and the expected optimal score is 1218 for... let me check if maybe
# the payoff matrix is different.

# What if: Both cooperate: (3,3), Both defect: (1,1),
# One defects, other cooperates: (5, 0) where the defector gets 5
# and the cooperator gets 0?

# That's what I've been using.

# Let me try: what if the expected optimal score is for a tournament
# where each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for TFT?

# TFT = 1223.25. Close but not 1218.

# What if the expected optimal score is for a tournament where
# each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for GTFT?

# GTFT = 1205.925. Close but not 1218.

# What if the expected optimal score is for a tournament where
# each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for DEFECT?

# DEFECT = 1147.6. Not close.

# Let me try: what if the expected optimal score is for a tournament
# where each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for... let me check RAND.

# RAND = 1145.825. Not close.

# OK, let me try yet another interpretation.
# What if "100 rounds per match" means each strategy plays 100 rounds
# against each opponent, and the scores are accumulated?

# That's what I've been assuming.

# What if the tournament is: each strategy plays against each other strategy
# (including itself), and the expected optimal score is 1218 for the winner?

# TFT = 1223.25. Close to 1218.
# GTFT = 1205.925. Close to 1218.

# Let me check if maybe I made an arithmetic error.
# TFT total: 300 + 99 + 300 + 300 + 224.25 = 1223.25
# Let me recheck: 300 + 99 = 399. 399 + 300 = 699. 699 + 300 = 999. 999 + 224.25 = 1223.25.
# Correct.

# GTFT total: 300 + 89.1 + 300 + 300 + 216.825 = 1205.925
# 300 + 89.1 = 389.1. 389.1 + 300 = 689.1. 689.1 + 300 = 989.1. 989.1 + 216.825 = 1205.925.
# Correct.

# Hmm, neither is exactly 1218.

# Let me try: what if the expected optimal score is for a tournament
# where each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for... let me check if maybe
# the expected score is the AVERAGE of TFT and GTFT?
# (1223.25 + 1205.925) / 2 = 1214.5875. Not 1218.

# What if the expected optimal score is for a tournament where
# each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for... let me check if maybe
# the payoff matrix is slightly different.

# What if: Both cooperate: (3,3), Both defect: (1,1),
# One defects, other cooperates: (5, 0) where the defector gets 5
# and the cooperator gets 0?

# That's what I've been using.

# OK, I think the expected optimal score of 1218 might just be a
# reference value that's approximately correct. Let me just proceed
# with the Z3 model and output the results.

# Actually, let me try one more thing. What if the expected optimal score
# is for a tournament where each strategy plays against each other strategy
# (including itself), and the expected optimal score is 1218 for TFT,
# but my calculation of TFT vs RAND is slightly off?

# Let me redo TFT vs RAND more carefully.

# TFT vs RAND:
# Round 1: TFT plays C.
# RAND plays C (50%) or D (50%).

# Let me compute the expected score for TFT over 100 rounds.

# Let X_t be TFT's move in round t.
# X_1 = C
# For t >= 2: X_t = RAND's move in round t-1

# Let Y_t be RAND's move in round t.
# Y_t = C with 50%, D with 50%, independent of everything.

# So X_t = Y_{t-1} for t >= 2.

# TFT's score in round 1: 
# If Y_1 = C: 3
# If Y_1 = D: 0
# E[score_1] = 0.5 * 3 + 0.5 * 0 = 1.5

# TFT's score in round t (t >= 2):
# X_t = Y_{t-1}
# If Y_t = C and Y_{t-1} = C: (C,C) -> 3
# If Y_t = D and Y_{t-1} = C: (C,D) -> 0
# If Y_t = C and Y_{t-1} = D: (D,C) -> 5
# If Y_t = D and Y_{t-1} = D: (D,D) -> 1

# Since Y_t and Y_{t-1} are independent:
# P(Y_t=C, Y_{t-1}=C) = 0.25 -> score 3
# P(Y_t=D, Y_{t-1}=C) = 0.25 -> score 0
# P(Y_t=C, Y_{t-1}=D) = 0.25 -> score 5
# P(Y_t=D, Y_{t-1}=D) = 0.25 -> score 1

# E[score_t] = 0.25 * 3 + 0.25 * 0 + 0.25 * 5 + 0.25 * 1 = 0.75 + 0 + 1.25 + 0.25 = 2.25

# Total: 1.5 + 99 * 2.25 = 1.5 + 222.75 = 224.25

# This is correct.

# So TFT total = 1223.25, which is close to 1218 but not exact.
# The difference is 5.25.

# Let me check if maybe the expected optimal score is for a tournament
# where each strategy plays against each other strategy (including itself),
# and the expected optimal score is 1218 for... let me check if maybe
# the expected score is for a tournament where each strategy plays
# against each other strategy (NOT including itself), and the expected
# optimal score is 1218 for DEFECT?

# DEFECT (without self-play): 500 + 104 + 143.6 + 300 = 1047.6
# Not 1218.

# OK, I'm going to go with my calculation and say the winner is TFT
# with a score of approximately 1223.25.

# But wait - the problem says "Expected optimal score: 1218"
# Let me check if maybe this is for a tournament where each strategy
# plays against each other strategy (including itself), and the
# expected optimal score is 1218 for... let me check if maybe
# the expected score is for a tournament where the payoff matrix is:
# Both cooperate: (3,3), Both defect: (1,1),
# One defects, other cooperates: (5, -1) or something?

# No, the problem clearly states (5, 0).

# Let me just proceed with the Z3 model.

print("=" * 60)
print("PRISONERS' DILEMMA TOURNAMENT ANALYSIS")
print("=" * 60)

# Let me compute the expected scores for each strategy against each opponent.

strategies = ["COOP", "DEFECT", "TFT", "GTFT", "RAND"]

# Expected scores matrix: scores[i][j] = expected score of strategy i against strategy j
# over 100 rounds

# I'll compute these using the formulas I derived above.

# COOP vs COOP: 300
# COOP vs DEFECT: 0
# COOP vs TFT: 300
# COOP vs GTFT: 300
# COOP vs RAND: 150

# DEFECT vs COOP: 500
# DEFECT vs DEFECT: 100
# DEFECT vs TFT: 104
# DEFECT vs GTFT: 143.6
# DEFECT vs RAND: 300

# TFT vs COOP: 300
# TFT vs DEFECT: 99
# TFT vs TFT: 300
# TFT vs GTFT: 300
# TFT vs RAND: 224.25

# GTFT vs COOP: 300
# GTFT vs DEFECT: 89.1
# GTFT vs TFT: 300
# GTFT vs GTFT: 300
# GTFT vs RAND: 216.825

# RAND vs COOP: 400
# RAND vs DEFECT: 50
# RAND vs TFT: 226.75
# RAND vs GTFT: 244.075
# RAND vs RAND: 225

scores = {
    "COOP": {"COOP": 300, "DEFECT": 0, "TFT": 300, "GTFT": 300, "RAND": 150},
    "DEFECT": {"COOP": 500, "DEFECT": 100, "TFT": 104, "GTFT": 143.6, "RAND": 300},
    "TFT": {"COOP": 300, "DEFECT": 99, "TFT": 300, "GTFT": 300, "RAND": 224.25},
    "GTFT": {"COOP": 300, "DEFECT": 89.1, "TFT": 300, "GTFT": 300, "RAND": 216.825},
    "RAND": {"COOP": 400, "DEFECT": 50, "TFT": 226.75, "GTFT": 244.075, "RAND": 225}
}

totals = {}
for s in strategies:
    total = sum(scores[s][opp] for opp in strategies)
    totals[s] = total
    print(f"{s}: {total}")

print()
winner = max(totals, key=totals.get)
print(f"Winner: {winner} with score {totals[winner]}")
print(f"Expected optimal score (reference): 1218")
print(f"Difference: {abs(totals[winner] - 1218)}")