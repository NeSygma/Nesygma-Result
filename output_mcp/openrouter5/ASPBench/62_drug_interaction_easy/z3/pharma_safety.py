from z3 import *

# ============================================================
# Problem Data
# ============================================================

# Patient
patient_conditions = ["pain", "hypertension", "diabetes"]
patient_contraindications = ["bleeding_disorder"]
max_drugs = 3

# Drugs: drug_id -> (treats, contraindications, max_dose, interactions)
# interactions: list of (other_drug_id, interaction_type, severity)
# severity: "severe", "moderate", "mild"
drugs_data = {
    "drug1": {
        "treats": ["pain", "inflammation"],
        "contraindications": ["bleeding_disorder"],
        "max_dose": 4000,
        "interactions": [("drug2", "increased_bleeding", "moderate")]
    },
    "drug2": {
        "treats": ["blood_clot_prevention"],
        "contraindications": ["pregnancy"],
        "max_dose": 10,
        "interactions": [("drug1", "increased_bleeding", "moderate")]
    },
    "drug3": {
        "treats": ["hypertension"],
        "contraindications": ["kidney_disease"],
        "max_dose": 40,
        "interactions": [("drug4", "mild_nausea", "mild")]
    },
    "drug4": {
        "treats": ["diabetes"],
        "contraindications": ["kidney_disease"],
        "max_dose": 2000,
        "interactions": [("drug3", "mild_nausea", "mild")]
    },
    "drug5": {
        "treats": ["pain", "inflammation"],
        "contraindications": [],
        "max_dose": 2400,
        "interactions": [("drug3", "reduced_bp_effect", "moderate")]
    }
}

drug_ids = list(drugs_data.keys())
num_drugs = len(drug_ids)

# Severity penalty mapping
severity_penalty = {"severe": 0.3, "moderate": 0.15, "mild": 0.05}

# ============================================================
# Z3 Model
# ============================================================

opt = Optimize()

# Decision variables:
# prescribe[i] = Bool indicating if drug i is prescribed
prescribe = [Bool(f"prescribe_{drug_ids[i]}") for i in range(num_drugs)]

# dose[i] = Int dose for drug i (only meaningful if prescribed)
dose = [Int(f"dose_{drug_ids[i]}") for i in range(num_drugs)]

# Constraint 1: Maximum drugs
opt.add(Sum([If(prescribe[i], 1, 0) for i in range(num_drugs)]) <= max_drugs)

# Constraint 2: Contraindications - cannot prescribe drugs that match patient's contraindications
for i, drug_id in enumerate(drug_ids):
    drug_contra = drugs_data[drug_id]["contraindications"]
    for pc in patient_contraindications:
        if pc in drug_contra:
            opt.add(Not(prescribe[i]))

# Constraint 3: Dosage - each prescribed drug must have dose between 1 and max_dose
for i, drug_id in enumerate(drug_ids):
    max_d = drugs_data[drug_id]["max_dose"]
    # If prescribed, dose in [1, max_dose]; if not prescribed, dose = 0
    opt.add(Implies(prescribe[i], And(dose[i] >= 1, dose[i] <= max_d)))
    opt.add(Implies(Not(prescribe[i]), dose[i] == 0))

# Constraint 4: Treatment coverage - we'll handle this via optimization objectives

# ============================================================
# Derived metrics for optimization
# ============================================================

# For each patient condition, is it treated?
# condition_treated[c] = Bool: True if at least one prescribed drug treats condition c
condition_treated = {}
for cond in patient_conditions:
    treats_cond = [prescribe[i] for i, drug_id in enumerate(drug_ids) if cond in drugs_data[drug_id]["treats"]]
    if treats_cond:
        condition_treated[cond] = Or(treats_cond)
    else:
        condition_treated[cond] = BoolVal(False)

# Number of treated conditions (as integer expression)
num_treated = Sum([If(condition_treated[cond], 1, 0) for cond in patient_conditions])
total_conditions = len(patient_conditions)

# Interaction detection and penalty
# For each pair of drugs (i, j) with i < j, check if both prescribed and have an interaction
interaction_penalties = []
interaction_details = []

for i in range(num_drugs):
    for j in range(i+1, num_drugs):
        drug_i = drug_ids[i]
        drug_j = drug_ids[j]
        # Check if drug_i has interaction with drug_j
        for (other, itype, severity) in drugs_data[drug_i]["interactions"]:
            if other == drug_j:
                penalty = severity_penalty[severity]
                both_prescribed = And(prescribe[i], prescribe[j])
                interaction_penalties.append(If(both_prescribed, penalty, 0))
                interaction_details.append((drug_i, drug_j, itype, severity, both_prescribed))
        # Check if drug_j has interaction with drug_i (should be symmetric, but check both)
        for (other, itype, severity) in drugs_data[drug_j]["interactions"]:
            if other == drug_i:
                # Avoid double-counting if already added
                if not any(d[0]==drug_i and d[1]==drug_j and d[2]==itype for d in interaction_details):
                    penalty = severity_penalty[severity]
                    both_prescribed = And(prescribe[i], prescribe[j])
                    interaction_penalties.append(If(both_prescribed, penalty, 0))
                    interaction_details.append((drug_i, drug_j, itype, severity, both_prescribed))

# Total penalty (as Real)
total_penalty = Sum(interaction_penalties)

# Coverage bonus
coverage_bonus = (num_treated / total_conditions) * 0.5

# Safety score
safety_score = 0.5 + coverage_bonus - total_penalty

# Clamp to [0, 1]
safety_score_clamped = If(safety_score < 0, 0.0, If(safety_score > 1, 1.0, safety_score))

# ============================================================
# Optimization Objectives
# ============================================================

# Primary objective: maximize number of treated conditions
opt.maximize(num_treated)

# Secondary objective: minimize total penalty (maximize negative penalty)
opt.minimize(total_penalty)

# ============================================================
# Solve
# ============================================================

BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    m = opt.model()
    
    # Extract prescription
    prescribed_list = []
    for i, drug_id in enumerate(drug_ids):
        if is_true(m.eval(prescribe[i])):
            d = int(m.eval(dose[i]).as_long())
            prescribed_list.append((drug_id, d))
    
    # Determine treated conditions
    treated_conds = []
    untreated_conds = []
    for cond in patient_conditions:
        if is_true(m.eval(condition_treated[cond])):
            treated_conds.append(cond)
        else:
            untreated_conds.append(cond)
    
    # Determine interactions
    detected_interactions = []
    for (d1, d2, itype, severity, both_expr) in interaction_details:
        if is_true(m.eval(both_expr)):
            detected_interactions.append({
                "drugs": [d1, d2],
                "type": itype,
                "severity": severity
            })
    
    # Calculate safety score numerically
    num_treated_val = m.eval(num_treated).as_long()
    total_penalty_val = float(m.eval(total_penalty).as_fraction())
    coverage_bonus_val = (num_treated_val / total_conditions) * 0.5
    safety_score_val = 0.5 + coverage_bonus_val - total_penalty_val
    safety_score_val = max(0.0, min(1.0, safety_score_val))
    
    print("STATUS: sat")
    print()
    print("=== OPTIMAL PRESCRIPTION ===")
    print(f"prescribed_drugs: {[{'drug_id': d, 'dose': dose, 'frequency': 'daily'} for d, dose in prescribed_list]}")
    print(f"treated_conditions: {treated_conds}")
    print(f"untreated_conditions: {untreated_conds}")
    print()
    print("=== SAFETY ANALYSIS ===")
    print(f"interactions_detected: {detected_interactions}")
    print(f"contraindications_avoided: {patient_contraindications}")
    print(f"safety_score: {safety_score_val:.4f}")
    print()
    print(f"Number of drugs prescribed: {len(prescribed_list)}")
    print(f"Number of conditions treated: {num_treated_val}/{total_conditions}")
    print(f"Total interaction penalty: {total_penalty_val:.4f}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")