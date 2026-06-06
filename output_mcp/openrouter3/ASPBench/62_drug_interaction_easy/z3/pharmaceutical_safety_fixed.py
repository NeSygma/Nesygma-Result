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
        "max_dose": 4000,
        "interactions": {"drug2": "moderate"}
    },
    "drug2": {
        "treats": ["blood_clot_prevention"],
        "contraindications": ["pregnancy"],
        "max_dose": 10,
        "interactions": {"drug1": "moderate"}
    },
    "drug3": {
        "treats": ["hypertension"],
        "contraindications": ["kidney_disease"],
        "max_dose": 40,
        "interactions": {"drug4": "mild"}
    },
    "drug4": {
        "treats": ["diabetes"],
        "contraindications": ["kidney_disease"],
        "max_dose": 2000,
        "interactions": {"drug3": "mild"}
    },
    "drug5": {
        "treats": ["pain", "inflammation"],
        "contraindications": [],
        "max_dose": 2400,
        "interactions": {"drug3": "moderate"}
    }
}

# Interaction severity penalties
severity_penalty = {"severe": 0.3, "moderate": 0.15, "mild": 0.05}

# Create optimizer
opt = Optimize()

# Decision variables
selected = {drug_id: Bool(f"selected_{drug_id}") for drug_id in drugs}
dose = {drug_id: Int(f"dose_{drug_id}") for drug_id in drugs}

# Constraint 1: Maximum drugs allowed
opt.add(Sum([If(selected[drug_id], 1, 0) for drug_id in drugs]) <= max_drugs)

# Constraint 2: No drugs matching patient contraindications
for drug_id, drug_data in drugs.items():
    if any(contraindication in patient_contraindications for contraindication in drug_data["contraindications"]):
        opt.add(Not(selected[drug_id]))

# Constraint 3: Dose constraints for selected drugs
for drug_id, drug_data in drugs.items():
    opt.add(Implies(selected[drug_id], And(dose[drug_id] >= 1, dose[drug_id] <= drug_data["max_dose"])))
    # For unselected drugs, dose can be anything (we'll ignore it)
    opt.add(Implies(Not(selected[drug_id]), dose[drug_id] == 0))

# Constraint 4: Treatment coverage - each condition must be treated
# A condition is treated if at least one selected drug treats it
for condition in patient_conditions:
    condition_treated = Or([
        And(selected[drug_id], condition in drugs[drug_id]["treats"])
        for drug_id in drugs
    ])
    opt.add(condition_treated)

# Interaction detection and penalty calculation
# We'll calculate total penalty as an integer (multiply by 100 to avoid fractions)
interaction_penalty_int = Int("interaction_penalty_int")
opt.add(interaction_penalty_int == 0)  # Start with 0, will add penalties

# Check all pairs of drugs for interactions
drug_list = list(drugs.keys())
for i in range(len(drug_list)):
    for j in range(i+1, len(drug_list)):
        drug1_id = drug_list[i]
        drug2_id = drug_list[j]
        
        # Check if both drugs are selected
        both_selected = And(selected[drug1_id], selected[drug2_id])
        
        # Check if there's an interaction between them
        has_interaction = False
        severity = None
        
        if drug2_id in drugs[drug1_id]["interactions"]:
            severity = drugs[drug1_id]["interactions"][drug2_id]
            has_interaction = True
        elif drug1_id in drugs[drug2_id]["interactions"]:
            severity = drugs[drug2_id]["interactions"][drug1_id]
            has_interaction = True
        
        if has_interaction:
            penalty = int(severity_penalty[severity] * 100)  # Multiply by 100 to avoid fractions
            # Add penalty if both drugs are selected
            opt.add(Implies(both_selected, interaction_penalty_int == interaction_penalty_int + penalty))

# Safety score calculation
total_conditions = len(patient_conditions)
treated_conditions_count = Sum([
    If(Or([And(selected[drug_id], condition in drugs[drug_id]["treats"]) for drug_id in drugs]), 1, 0)
    for condition in patient_conditions
])

# For optimization: maximize treated conditions, then minimize interaction penalty
# We'll use a weighted objective: maximize (treated_conditions * 1000 - interaction_penalty_int)
# This ensures treated conditions are prioritized
objective = treated_conditions_count * 1000 - interaction_penalty_int
opt.maximize(objective)

result = opt.check()
if result == sat:
    model = opt.model()
    
    print("STATUS: sat")
    
    # Extract solution
    prescribed_drugs = []
    for drug_id in drugs:
        if is_true(model[selected[drug_id]]):
            dose_value = model[dose[drug_id]].as_long()
            prescribed_drugs.append({
                "drug_id": drug_id,
                "dose": dose_value,
                "frequency": "as needed"  # Default frequency
            })
    
    # Determine treated conditions
    treated_conditions = []
    untreated_conditions = []
    for condition in patient_conditions:
        is_treated = any(
            condition in drugs[drug["drug_id"]]["treats"] 
            for drug in prescribed_drugs
        )
        if is_treated:
            treated_conditions.append(condition)
        else:
            untreated_conditions.append(condition)
    
    # Detect interactions
    interactions_detected = []
    total_penalty = 0
    for i in range(len(prescribed_drugs)):
        for j in range(i+1, len(prescribed_drugs)):
            drug1_id = prescribed_drugs[i]["drug_id"]
            drug2_id = prescribed_drugs[j]["drug_id"]
            
            severity = None
            if drug2_id in drugs[drug1_id]["interactions"]:
                severity = drugs[drug1_id]["interactions"][drug2_id]
            elif drug1_id in drugs[drug2_id]["interactions"]:
                severity = drugs[drug2_id]["interactions"][drug1_id]
            
            if severity:
                interactions_detected.append({
                    "drugs": [drug1_id, drug2_id],
                    "severity": severity
                })
                total_penalty += severity_penalty[severity]
    
    # Calculate safety score
    coverage_bonus_value = (len(treated_conditions) / total_conditions) * 0.5
    safety_score_value = 0.5 + coverage_bonus_value - total_penalty
    safety_score_clamped_value = max(0, min(1, safety_score_value))
    
    # Print results
    print("\nPrescription:")
    for drug in prescribed_drugs:
        print(f"  {drug['drug_id']}: {drug['dose']} mg, {drug['frequency']}")
    
    print(f"\nTreated conditions: {treated_conditions}")
    print(f"Untreated conditions: {untreated_conditions}")
    
    print(f"\nSafety Analysis:")
    print(f"  Interactions detected: {interactions_detected}")
    print(f"  Contraindications avoided: {patient_contraindications}")
    print(f"  Safety score: {safety_score_clamped_value:.3f}")
    
    # Verify expected solution
    expected_drugs = {"drug4", "drug5"}
    actual_drugs = {drug["drug_id"] for drug in prescribed_drugs}
    if (actual_drugs == expected_drugs and
        set(treated_conditions) == {"diabetes", "pain"} and
        len(interactions_detected) == 0):
        print("\n✓ Expected optimal solution found!")
    else:
        print(f"\nNote: Solution differs from expected")
        print(f"  Expected drugs: {expected_drugs}")
        print(f"  Actual drugs: {actual_drugs}")
        
else:
    print("STATUS: unsat")
    print("No solution found")