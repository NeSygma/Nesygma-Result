from z3 import *

# Patient data
patient_conditions = ["pain", "hypertension", "diabetes"]
patient_contraindications = ["bleeding_disorder"]
max_drugs_allowed = 3
NUM_CONDITIONS = len(patient_conditions)

# Drug data (using drug IDs)
drug_ids = ["drug1", "drug2", "drug3", "drug4", "drug5"]
drug_treats = [
    ["pain", "inflammation"],           # drug1
    ["blood_clot_prevention"],          # drug2
    ["hypertension"],                   # drug3
    ["diabetes"],                       # drug4
    ["pain", "inflammation"],           # drug5
]
drug_contraindications = [
    ["bleeding_disorder"],  # drug1
    ["pregnancy"],          # drug2
    ["kidney_disease"],     # drug3
    ["kidney_disease"],     # drug4
    [],                     # drug5
]
drug_max_dose = [4000, 10, 40, 2000, 2400]

NUM_DRUGS = len(drug_ids)

# Interactions: (i, j, severity, penalty_value)
interactions = [
    (0, 1, 0.15),  # drug1-drug2: moderate
    (2, 3, 0.05),  # drug3-drug4: mild
    (2, 4, 0.15),  # drug3-drug5: moderate
]

opt = Optimize()

# Decision variables
use = [Bool(f"use_{drug_ids[i]}") for i in range(NUM_DRUGS)]
dose = [Int(f"dose_{drug_ids[i]}") for i in range(NUM_DRUGS)]

# Constraint 1: Max drugs
opt.add(Sum([If(use[i], 1, 0) for i in range(NUM_DRUGS)]) <= max_drugs_allowed)

# Constraint 2: Contraindications
for i in range(NUM_DRUGS):
    for ci in drug_contraindications[i]:
        if ci in patient_contraindications:
            opt.add(Not(use[i]))

# Constraint 3: Dosage bounds
for i in range(NUM_DRUGS):
    opt.add(Implies(use[i], And(dose[i] >= 1, dose[i] <= drug_max_dose[i])))
    opt.add(Implies(Not(use[i]), dose[i] == 0))

# Treatment coverage
treated = [Bool(f"treated_{c}") for c in patient_conditions]
for j, cond in enumerate(patient_conditions):
    treating_drugs = [use[i] for i in range(NUM_DRUGS) if cond in drug_treats[i]]
    if treating_drugs:
        opt.add(treated[j] == Or(treating_drugs))
    else:
        opt.add(treated[j] == False)

treated_count = Sum([If(treated[j], 1, 0) for j in range(NUM_CONDITIONS)])

# Interaction penalty
penalty_terms = []
for (i, j, penalty_val) in interactions:
    penalty_terms.append(If(And(use[i], use[j]), RealVal(penalty_val), RealVal(0)))
total_penalty = Sum(penalty_terms)

# Safety score calculation
safety_score = Real('safety_score')
opt.add(safety_score == 0.5 + (ToReal(treated_count) / RealVal(NUM_CONDITIONS)) * 0.5 - total_penalty)

# Clamp to [0, 1]
opt.add(safety_score >= 0)
opt.add(safety_score <= 1)

# Maximize safety score
opt.maximize(safety_score)

result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    
    # Extract prescribed drugs
    prescribed_indices = []
    prescribed_info = []
    for i in range(NUM_DRUGS):
        if is_true(m.eval(use[i])):
            prescribed_indices.append(i)
            dose_val = m.eval(dose[i]).as_long()
            prescribed_info.append({"drug_id": drug_ids[i], "dose": dose_val, "frequency": "daily"})
            print(f"  Prescribed: {drug_ids[i]}, dose = {dose_val} mg")
    
    # Extract treated/untreated conditions
    treated_list = []
    untreated_list = []
    for j, cond in enumerate(patient_conditions):
        if is_true(m.eval(treated[j])):
            treated_list.append(cond)
        else:
            untreated_list.append(cond)
    
    print(f"\n  Treated conditions: {treated_list}")
    print(f"  Untreated conditions: {untreated_list}")
    
    # Detect interactions
    detected_interactions = []
    for (i, j, penalty_val) in interactions:
        if is_true(m.eval(And(use[i], use[j]))):
            sev = "moderate" if penalty_val == 0.15 else "mild" if penalty_val == 0.05 else "severe"
            detected_interactions.append({"drugs": [drug_ids[i], drug_ids[j]], "severity": sev})
            print(f"  Interaction: {drug_ids[i]} - {drug_ids[j]}: {sev}")
    
    # Safety score - convert rational to float
    score_val = m.eval(safety_score)
    score_str = str(score_val)
    if '/' in score_str:
        num, den = score_str.split('/')
        score_float = float(num) / float(den)
    else:
        score_float = float(score_str)
    
    print(f"\n  Safety score: {score_float:.4f}")
    print(f"\n--- Output Fields ---")
    print(f"prescribed_drugs: {prescribed_info}")
    print(f"treated_conditions: {treated_list}")
    print(f"untreated_conditions: {untreated_list}")
    print(f"safety_analysis.interactions_detected: {detected_interactions}")
    print(f"safety_analysis.contraindications_avoided: {patient_contraindications}")
    print(f"safety_analysis.safety_score: {score_float:.4f}")
else:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat")