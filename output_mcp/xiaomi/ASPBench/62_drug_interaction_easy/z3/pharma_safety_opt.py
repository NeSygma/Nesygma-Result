from z3 import *

# Problem data
patient_conditions = ["pain", "hypertension", "diabetes"]
patient_contraindications = ["bleeding_disorder"]
max_drugs = 3

# Drug data
drugs = {
    "drug1": {
        "treats": ["pain", "inflammation"],
        "contraindications": ["bleeding_disorder"],
        "max_dose": 4000
    },
    "drug2": {
        "treats": ["blood_clot_prevention"],
        "contraindications": ["pregnancy"],
        "max_dose": 10
    },
    "drug3": {
        "treats": ["hypertension"],
        "contraindications": ["kidney_disease"],
        "max_dose": 40
    },
    "drug4": {
        "treats": ["diabetes"],
        "contraindications": ["kidney_disease"],
        "max_dose": 2000
    },
    "drug5": {
        "treats": ["pain", "inflammation"],
        "contraindications": [],
        "max_dose": 2400
    }
}

# Drug interactions (bidirectional)
interactions = {
    ("drug1", "drug2"): {"effect": "increased_bleeding", "severity": "moderate"},
    ("drug2", "drug1"): {"effect": "increased_bleeding", "severity": "moderate"},
    ("drug3", "drug4"): {"effect": "mild_nausea", "severity": "mild"},
    ("drug4", "drug3"): {"effect": "mild_nausea", "severity": "mild"},
    ("drug5", "drug3"): {"effect": "reduced_bp_effect", "severity": "moderate"},
    ("drug3", "drug5"): {"effect": "reduced_bp_effect", "severity": "moderate"}
}

# Create Z3 optimizer
opt = Optimize()

# Decision variables: whether each drug is prescribed
prescribed = {drug: Bool(f"prescribed_{drug}") for drug in drugs}

# Dose variables for each drug (0 if not prescribed)
dose = {drug: Int(f"dose_{drug}") for drug in drugs}

# Condition treated variables
condition_treated = {cond: Bool(f"treated_{cond}") for cond in patient_conditions}

# Interaction variables
interaction_vars = {}
for (d1, d2), info in interactions.items():
    if d1 < d2:  # Only create one variable per pair
        interaction_vars[(d1, d2)] = {
            "occurs": Bool(f"interaction_{d1}_{d2}"),
            "severity": info["severity"],
            "effect": info["effect"]
        }

# Constraints

# 1. Maximum drugs constraint
opt.add(Sum([If(prescribed[drug], 1, 0) for drug in drugs]) <= max_drugs)

# 2. Contraindication constraints
for drug in drugs:
    # Check if drug has any contraindication that matches patient's contraindications
    has_contraindication = False
    for contra in drugs[drug]["contraindications"]:
        if contra in patient_contraindications:
            has_contraindication = True
            break
    if has_contraindication:
        opt.add(Not(prescribed[drug]))

# 3. Dosage constraints
for drug in drugs:
    # If prescribed, dose must be between 1 and max_dose
    opt.add(Implies(prescribed[drug], And(dose[drug] >= 1, dose[drug] <= drugs[drug]["max_dose"])))
    # If not prescribed, dose must be 0
    opt.add(Implies(Not(prescribed[drug]), dose[drug] == 0))

# 4. Treatment coverage constraints
for cond in patient_conditions:
    # A condition is treated if at least one prescribed drug treats it
    treating_drugs = [drug for drug in drugs if cond in drugs[drug]["treats"]]
    opt.add(condition_treated[cond] == Or([And(prescribed[drug], True) for drug in treating_drugs]))

# 5. Interaction constraints
for (d1, d2), var_info in interaction_vars.items():
    # Interaction occurs if both drugs are prescribed
    opt.add(var_info["occurs"] == And(prescribed[d1], prescribed[d2]))

# Objective: Maximize treated conditions, minimize interaction severity
# We'll use a weighted objective
treated_count = Sum([If(condition_treated[cond], 1, 0) for cond in patient_conditions])

# Calculate interaction penalty
interaction_penalty = 0
for (d1, d2), var_info in interaction_vars.items():
    if var_info["severity"] == "severe":
        interaction_penalty += If(var_info["occurs"], 3, 0)
    elif var_info["severity"] == "moderate":
        interaction_penalty += If(var_info["occurs"], 2, 0)
    elif var_info["severity"] == "mild":
        interaction_penalty += If(var_info["occurs"], 1, 0)

# Maximize: treated_count * 10 - interaction_penalty (to prioritize coverage)
opt.maximize(treated_count * 10 - interaction_penalty)

# Check satisfiability
BENCHMARK_MODE = True
result = opt.check()

if result == sat:
    model = opt.model()
    print("STATUS: sat")
    
    # Extract prescribed drugs
    prescribed_drugs = []
    for drug in drugs:
        if is_true(model[prescribed[drug]]):
            dose_val = model[dose[drug]].as_long()
            prescribed_drugs.append({
                "drug_id": drug,
                "dose": dose_val,
                "frequency": "once daily"  # Default frequency
            })
    
    # Extract treated conditions
    treated_conditions = []
    untreated_conditions = []
    for cond in patient_conditions:
        if is_true(model[condition_treated[cond]]):
            treated_conditions.append(cond)
        else:
            untreated_conditions.append(cond)
    
    # Extract interactions
    interactions_detected = []
    for (d1, d2), var_info in interaction_vars.items():
        if is_true(model[var_info["occurs"]]):
            interactions_detected.append({
                "drugs": [d1, d2],
                "effect": var_info["effect"],
                "severity": var_info["severity"]
            })
    
    # Calculate safety score
    total_conditions = len(patient_conditions)
    coverage_bonus = (len(treated_conditions) / total_conditions) * 0.5
    
    total_penalty = 0
    for interaction in interactions_detected:
        if interaction["severity"] == "severe":
            total_penalty += 0.3
        elif interaction["severity"] == "moderate":
            total_penalty += 0.15
        elif interaction["severity"] == "mild":
            total_penalty += 0.05
    
    safety_score = 0.5 + coverage_bonus - total_penalty
    safety_score = max(0.0, min(1.0, safety_score))
    
    # Print results
    print("\n=== Prescription Analysis ===")
    print(f"Prescribed drugs ({len(prescribed_drugs)}):")
    for drug_info in prescribed_drugs:
        print(f"  - {drug_info['drug_id']}: {drug_info['dose']} mg, {drug_info['frequency']}")
    
    print(f"\nTreated conditions ({len(treated_conditions)}): {treated_conditions}")
    print(f"Untreated conditions ({len(untreated_conditions)}): {untreated_conditions}")
    
    print(f"\n=== Safety Analysis ===")
    print(f"Interactions detected ({len(interactions_detected)}):")
    for interaction in interactions_detected:
        print(f"  - {interaction['drugs'][0]} + {interaction['drugs'][1]}: {interaction['effect']} ({interaction['severity']})")
    
    print(f"Contraindications avoided: {patient_contraindications}")
    print(f"Safety score: {safety_score:.2f}")
    
    # Print summary
    print(f"\n=== Summary ===")
    print(f"Total drugs prescribed: {len(prescribed_drugs)}")
    print(f"Conditions treated: {len(treated_conditions)}/{total_conditions}")
    print(f"Interaction penalty: {total_penalty}")
    print(f"Coverage bonus: {coverage_bonus:.2f}")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")