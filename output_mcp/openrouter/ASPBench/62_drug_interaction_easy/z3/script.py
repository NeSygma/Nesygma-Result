from z3 import *

# Data
drug_ids = ["drug1", "drug2", "drug3", "drug4", "drug5"]
max_dose = [4000, 10, 40, 2000, 2400]
# contraindications per drug (list of strings)
drug_contra = [ ["bleeding_disorder"], ["pregnancy"], ["kidney_disease"], ["kidney_disease"], [] ]
# treats per drug
drug_treats = [ ["pain", "inflammation"], ["blood_clot_prevention"], ["hypertension"], ["diabetes"], ["pain", "inflammation"] ]
# interactions: (i,j): severity string
interactions = { (0,1): "moderate", (2,3): "mild", (4,2): "moderate" }
severity_weight = {"severe": 0.3, "moderate": 0.15, "mild": 0.05}

patient_conditions = ["pain", "hypertension", "diabetes"]
patient_contra = ["bleeding_disorder"]
max_drugs_allowed = 3

# Solver
opt = Optimize()
# decision variables
selected = [Bool(f"sel_{i}") for i in range(len(drug_ids))]
dose = [Int(f"dose_{i}") for i in range(len(drug_ids))]

# Constraints
# max drugs
opt.add(Sum([If(selected[i], 1, 0) for i in range(len(drug_ids))]) <= max_drugs_allowed)
# contraindications: cannot select drug if any of its contraindications intersect patient_contra
for i in range(len(drug_ids)):
    for pc in patient_contra:
        if pc in drug_contra[i]:
            opt.add(selected[i] == False)
# dosage constraints
for i in range(len(drug_ids)):
    # if selected then dose between 1 and max_dose, else dose == 0
    opt.add(If(selected[i], And(dose[i] >= 1, dose[i] <= max_dose[i]), dose[i] == 0))

# Treatment coverage: compute treated condition count (as expression)
# For each condition, check if any selected drug treats it
treated_flags = []
for cond in patient_conditions:
    treats_cond = []
    for i in range(len(drug_ids)):
        if cond in drug_treats[i]:
            treats_cond.append(selected[i])
    if treats_cond:
        treated_flags.append(Or(treats_cond))
    else:
        treated_flags.append(False)
treated_count = Sum([If(flag, 1, 0) for flag in treated_flags])

# Interaction penalty
penalty_terms = []
for (i,j), sev in interactions.items():
    both = And(selected[i], selected[j])
    weight = severity_weight[sev]
    penalty_terms.append(If(both, RealVal(weight), RealVal(0)))
total_penalty = Sum(penalty_terms)

# Objectives: maximize treated_count, then minimize total_penalty
opt.maximize(treated_count)
opt.minimize(total_penalty)

# Solve
res = opt.check()
if res == sat:
    m = opt.model()
    # Build output structures
    prescribed = []
    for i in range(len(drug_ids)):
        if is_true(m.eval(selected[i])):
            prescribed.append({"drug_id": drug_ids[i], "dose": m.eval(dose[i]).as_long()})
    # Treated and untreated conditions
    treated = []
    untreated = []
    for idx, cond in enumerate(patient_conditions):
        flag = m.eval(treated_flags[idx])
        if is_true(flag):
            treated.append(cond)
        else:
            untreated.append(cond)
    # Interactions detected
    interactions_detected = []
    for (i,j), sev in interactions.items():
        if is_true(m.eval(And(selected[i], selected[j]))):
            interactions_detected.append({"drugs": [drug_ids[i], drug_ids[j]], "severity": sev})
    # Safety score
    coverage_bonus = (len(treated) / len(patient_conditions)) * 0.5
    total_pen = float(m.eval(total_penalty).as_decimal(10))
    safety_score = 0.5 + coverage_bonus - total_pen
    if safety_score < 0: safety_score = 0.0
    if safety_score > 1: safety_score = 1.0
    # Output
    print("STATUS: sat")
    print("prescribed_drugs =", prescribed)
    print("treated_conditions =", treated)
    print("untreated_conditions =", untreated)
    print("safety_analysis.interactions_detected =", interactions_detected)
    print("safety_analysis.contraindications_avoided =", patient_contra)
    print(f"safety_analysis.safety_score = {safety_score:.6f}")
else:
    print("STATUS: unsat")