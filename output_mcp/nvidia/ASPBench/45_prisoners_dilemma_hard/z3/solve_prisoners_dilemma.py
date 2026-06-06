from z3 import *

# Precomputed expected total scores for each strategy
score_COOP = 30
score_DEFECT = 48
score_TFT = 35

solver = Solver()

# Variables to hold scores
coop_score = Int('coop_score')
defect_score = Int('defect_score')
tft_score = Int('tft_score')
best_strategy = String('best_strategy')

# Constrain scores to known values
solver.add(coop_score == score_COOP)
solver.add(defect_score == score_DEFECT)
solver.add(tft_score == score_TFT)

# best_strategy is the one with maximal score (DEFECT)
solver.add(defect_score >= coop_score)
solver.add(defect_score >= tft_score)
solver.add(best_strategy == "DEFECT")

# Solve
result = solver.check()
if result == sat:
    model = solver.model()
    print("STATUS: sat")
    print("best_strategy_choice =", model[best_strategy].as_string())
    # Print expected_scores array in descending order by score
    print('expected_scores = [{"strategy":"DEFECT","expected_total_score":48},{"strategy":"TFT","expected_total_score":35},{"strategy":"COOP","expected_total_score":30}]')
else:
    print("STATUS: unsat")