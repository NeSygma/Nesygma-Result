from z3 import *

# Problem data
BENCHMARK_MODE = True

# Drug information
drug_ids = ['drug1','drug2','drug3','drug4','drug5']
max_doses = [4000,10,40,2000,2400]
# Treats mapping
# 0: drug1 treats pain
# 1: drug2 none relevant
# 2: drug3 treats hypertension
# 3: drug4 treats diabetes
# 4: drug5 treats pain

# Interaction data: (i,j,severity)
interaction_pairs = [
    (0,1,'moderate'),  # drug1-drug2
    (2,3,'mild'),      # drug3-drug4
    (4,2,'moderate')   # drug5-drug3
]
# Penalty mapping
penalty_map = {
    'severe': RealVal(0.3),
    'moderate': RealVal(0.15),
    'mild': RealVal(0.05)
}

solver = Optimize()

# Variables
selected = [Bool(f'sel_{i}') for i in range(5)]
dose = [Int(f'dose_{i}') for i in range(5)]

# Contraindication: patient has bleeding_disorder, drug1 has this contraindication
solver.add(selected[0] == False)

# Dose constraints
for i in range(5):
    solver.add(Implies(selected[i], And(dose[i] >= 1, dose[i] <= max_doses[i])))
    solver.add(Implies(Not(selected[i]), dose[i] == 0))

# Max drugs allowed
solver.add(Sum([If(selected[i], 1, 0) for i in range(5)]) <= 3)

# Treatment coverage
pain_treated = Or(selected[0], selected[4])
hypertension_treated = selected[2]
diabetes_treated = selected[3]

treated_count = Sum([If(pain_treated, 1, 0), If(hypertension_treated, 1, 0), If(diabetes_treated, 1, 0)])

# Interaction penalties
penalties = []
for (i,j,severe) in interaction_pairs:
    penalty = penalty_map[severe]
    penalties.append(If(And(selected[i], selected[j]), penalty, RealVal(0)))

total_penalty = Sum(penalties)

# Safety score calculation
coverage_bonus = (ToReal(treated_count) / RealVal(3)) * RealVal(0.5)
safety_score = RealVal(0.5) + coverage_bonus - total_penalty
safety_score_clamped = If(safety_score < 0, 0, If(safety_score > 1, 1, safety_score))

# Objectives: maximize treated conditions, minimize penalty
solver.maximize(treated_count)
solver.minimize(total_penalty)

# Check
result = solver.check()
if result == sat:
    model = solver.model()
    # Gather prescription
    prescribed = []
    for i in range(5):
        if is_true(model.eval(selected[i])):
            prescribed.append((drug_ids[i], model.eval(dose[i]).as_long()))
    # Treated conditions list
    treated = []
    if is_true(model.eval(pain_treated)):
        treated.append('pain')
    if is_true(model.eval(hypertension_treated)):
        treated.append('hypertension')
    if is_true(model.eval(diabetes_treated)):
        treated.append('diabetes')
    untreated = ['pain','hypertension','diabetes']
    for c in treated:
        if c in untreated:
            untreated.remove(c)
    # Interactions detected
    interactions = []
    for (i,j,severe) in interaction_pairs:
        if is_true(model.eval(selected[i])) and is_true(model.eval(selected[j])):
            interactions.append(f"{drug_ids[i]}-{drug_ids[j]} ({severe})")
    # Safety score value
    score_val = model.eval(safety_score_clamped)
    # Convert to float
    if score_val.is_real():
        s_str = score_val.as_decimal(10)
        if s_str.endswith('?'):
            s_str = s_str[:-1]
        score_float = float(s_str)
    else:
        score_float = float(score_val.as_long())
    # Output
    print("STATUS: sat")
    # prescribed_drugs
    pres_str = ", ".join([f"{d[0]} {d[1]} mg" for d in prescribed])
    print(f"prescribed_drugs: {pres_str}")
    # treated_conditions
    print("treated_conditions: " + ", ".join(treated))
    # untreated_conditions
    if untreated:
        print("untreated_conditions: " + ", ".join(untreated))
    else:
        print("untreated_conditions: (none)")
    # interactions_detected
    if interactions:
        print("safety_analysis.interactions_detected: " + ", ".join(interactions))
    else:
        print("safety_analysis.interactions_detected: (none)")
    # contraindications_avoided
    print("safety_analysis.contraindications_avoided: bleeding_disorder")
    # safety_score
    print(f"safety_analysis.safety_score: {score_float:.2f}")
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")