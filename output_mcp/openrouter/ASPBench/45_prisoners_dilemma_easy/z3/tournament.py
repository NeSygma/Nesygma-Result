from z3 import *

# Define expected total scores per match (100 rounds) for each ordered pair.
# Using RealVal for exact rational numbers.
# Strategies: COOP, DEFECT, TFT, GTFT, RAND

# Helper to create RealVal from float with exact rational representation

def rv(x):
    return RealVal(str(x))

# Payoffs per match (first player score, second player score)
# Self matches
coop_coop = (rv(300), rv(300))
defect_defect = (rv(100), rv(100))
tft_tft = (rv(300), rv(300))
gtft_gtft = (rv(300), rv(300))
rand_rand = (rv(225), rv(225))

# COOP vs others
coop_defect = (rv(0), rv(500))
coop_tft = (rv(300), rv(300))
coop_gtft = (rv(300), rv(300))
coop_rand = (rv(150), rv(400))

# DEFECT vs others (excluding COOP already covered)
defect_tft = (rv(104), rv(99))  # first is DEFECT, second TFT
# GTFT vs DEFECT (first GTFT, second DEFECT) same as earlier values

defect_gtft = (rv(143.6), rv(89.1))

defect_rand = (rv(300), rv(50))

# TFT vs others (excluding COOP, DEFECT already covered)
tft_gtft = (rv(300), rv(300))
tft_rand = (rv(224.25), rv(226.75))

# GTFT vs others (excluding COOP, DEFECT, TFT already covered)
gtft_rand = (rv(216.825), rv(244.075))

# Build totals for each strategy by summing appropriate components.
# We'll use Z3 expressions.

# Initialize totals as RealVal(0)
coop_total = rv(0)
defect_total = rv(0)
tft_total = rv(0)
gtft_total = rv(0)
rand_total = rv(0)

# Add self matches
coop_total += coop_coop[0]
coop_total += coop_coop[1]  # both sides get same, but we need only coop's own score, so add once? Actually self match both players are same strategy, each gets its own payoff. For coop_total we add coop's payoff (300). Not both.
# Correction: For self match, each strategy gets its own payoff once.
# So we should add only the first component (which equals second) for each strategy.
# We'll adjust below.

# Reset and recompute correctly.
coop_total = rv(0)
defect_total = rv(0)
tft_total = rv(0)
gtft_total = rv(0)
rand_total = rv(0)

# Self matches
coop_total += coop_coop[0]
defect_total += defect_defect[0]
tft_total += tft_tft[0]
gtft_total += gtft_gtft[0]
rand_total += rand_rand[0]

# COOP vs others (COOP as first player)
coop_total += coop_defect[0]
defect_total += coop_defect[1]
coop_total += coop_tft[0]
tft_total += coop_tft[1]
coop_total += coop_gtft[0]
gtft_total += coop_gtft[1]
coop_total += coop_rand[0]
rand_total += coop_rand[1]

# DEFECT vs others (DEFECT as first player) - COOP already accounted
# DEFECT vs TFT

defect_total += defect_tft[0]
tft_total += defect_tft[1]
# DEFECT vs GTFT

defect_total += defect_gtft[0]
gtft_total += defect_gtft[1]
# DEFECT vs RAND

defect_total += defect_rand[0]
rand_total += defect_rand[1]

# TFT vs others (TFT as first) - COOP, DEFECT already accounted
# TFT vs GTFT

tft_total += tft_gtft[0]
gtft_total += tft_gtft[1]
# TFT vs RAND

tft_total += tft_rand[0]
rand_total += tft_rand[1]

# GTFT vs RAND (GTFT first)
gtft_total += gtft_rand[0]
rand_total += gtft_rand[1]

# No need to add RAND vs others as first because already accounted when they were second.

# Solver (no constraints needed, just to satisfy framework)
solver = Solver()
result = solver.check()
if result == sat:
    m = solver.model()
    # Evaluate totals
    ct = m.eval(coop_total, model_completion=True)
    dt = m.eval(defect_total, model_completion=True)
    tt = m.eval(tft_total, model_completion=True)
    gt = m.eval(gtft_total, model_completion=True)
    rt = m.eval(rand_total, model_completion=True)
    # Convert to float for sorting
    def to_float(val):
        return float(val.numerator_as_long())/float(val.denominator_as_long())
    scores = {
        'COOP': to_float(ct),
        'DEFECT': to_float(dt),
        'TFT': to_float(tt),
        'GTFT': to_float(gt),
        'RAND': to_float(rt)
    }
    # Sort descending
    sorted_scores = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    print('STATUS: sat')
    print('tournament_results:', sorted_scores)
    print('winner:', sorted_scores[0][0])
else:
    print('STATUS: unsat')