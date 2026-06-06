from z3 import *

# ============================================================================
# Problem Data
# ============================================================================

# Patient data
patient_conditions = ["pain", "hypertension", "diabetes"]
patient_contraindications = ["bleeding_disorder"]
max_drugs = 3

# Drug data: each drug is a dict with keys: drug_id, treats, contraindications, max_dose, interactions
# Interactions: list of tuples (other_drug_id, severity)
drugs_data = [
    {
        "drug_id": "drug1",
        "treats": ["pain", "inflammation"],
        "contraindications": ["bleeding_disorder"],
        "max_dose": 4000,
        "interactions": [("drug2", "moderate")],
    },
    {
        "drug_id": "drug2",
        "treats": ["blood_clot_prevention"],
        "contraindications": ["pregnancy"],
        "max_dose": 10,
        "interactions": [("drug1", "moderate")],
    },
    {
        "drug_id": "drug3",
        "treats": ["hypertension"],
        "contraindications": ["kidney_disease"],
        "max_dose": 40,
        "interactions": [("drug4", "mild")],
    },
    {
        "drug_id": "drug4",
        "treats": ["diabetes"],
        "contraindications": ["kidney_disease"],
        "max_dose": 2000,
        "interactions": [("drug3", "mild")],
    },
    {
        "drug_id": "drug5",
        "treats": ["pain", "inflammation"],
        "contraindications": [],
        "max_dose": 2400,
        "interactions": [("drug3", "moderate")],
    },
]

# ============================================================================
# Helper Functions
# ============================================================================

def get_drug_by_id(drug_id):
    for drug in drugs_data:
        if drug["drug_id"] == drug_id:
            return drug
    return None

# ============================================================================
# Z3 Model
# ============================================================================

# Create an Optimize instance to maximize coverage and minimize penalties
opt = Optimize()

# Decision variables:
# - selected[i]: whether drug i is selected (Bool)
# - dose[i]: dose of drug i (Int)
# - frequency[i]: frequency of drug i (Int)
# - treated[c]: whether condition c is treated (Bool)

selected = [Bool(f"selected_{drug['drug_id']}") for drug in drugs_data]
dose = [Int(f"dose_{drug['drug_id']}") for drug in drugs_data]
frequency = [Int(f"freq_{drug['drug_id']}") for drug in drugs_data]

# Condition coverage variables
condition_vars = {cond: Bool(f"treated_{cond}") for cond in patient_conditions}

# ============================================================================
# Constraints
# ============================================================================

# 1. Maximum drugs constraint: at most max_drugs drugs can be selected
opt.add(Sum(selected) <= max_drugs)

# 2. Contraindications: cannot select a drug with a contraindication matching patient's contraindications
for i, drug in enumerate(drugs_data):
    for contra in drug["contraindications"]:
        if contra in patient_contraindications:
            opt.add(Not(selected[i]))

# 3. Dosage: dose must be between 1 and max_dose
for i, drug in enumerate(drugs_data):
    opt.add(dose[i] >= 1)
    opt.add(dose[i] <= drug["max_dose"])

# 4. Frequency: assume frequency is at least 1 (can be adjusted)
for i in range(len(drugs_data)):
    opt.add(frequency[i] >= 1)

# 5. Treatment coverage: a condition is treated if at least one selected drug treats it
for cond in patient_conditions:
    # At least one selected drug treats this condition
    drugs_that_treat = [
        selected[i] for i, drug in enumerate(drugs_data) if cond in drug["treats"]
    ]
    opt.add(Implies(Or(drugs_that_treat), condition_vars[cond]))
    opt.add(Implies(Not(Or(drugs_that_treat)), Not(condition_vars[cond])))

# ============================================================================
# Interaction Detection and Penalty Calculation
# ============================================================================

# Interaction penalty variables: penalty for each possible interaction
interaction_penalties = []
interactions_detected = []

# For each pair of drugs, check if they interact
for i in range(len(drugs_data)):
    for j in range(i + 1, len(drugs_data)):
        drug1 = drugs_data[i]
        drug2 = drugs_data[j]
        
        # Check if drug1 and drug2 interact
        for (other_id, severity) in drug1["interactions"]:
            if other_id == drug2["drug_id"]:
                # Interaction detected
                penalty = 0
                if severity == "severe":
                    penalty = -0.3
                elif severity == "moderate":
                    penalty = -0.15
                elif severity == "mild":
                    penalty = -0.05
                
                # Only add penalty if both drugs are selected
                penalty_var = Real(f"penalty_{drug1['drug_id']}_{drug2['drug_id']}")
                opt.add(penalty_var == If(And(selected[i], selected[j]), penalty, 0))
                interaction_penalties.append(penalty_var)
                interactions_detected.append((drug1["drug_id"], drug2["drug_id"], severity))
                break

# ============================================================================
# Objective: Maximize coverage and minimize penalties
# ============================================================================

# Coverage bonus: (number of treated conditions / total conditions) * 0.5
coverage_bonus = (Sum([If(condition_vars[cond], 1, 0) for cond in patient_conditions]) / len(patient_conditions)) * 0.5

# Total penalty: sum of all interaction penalties
total_penalty = Sum(interaction_penalties)

# Safety score: 0.5 + coverage_bonus + total_penalty (since penalties are negative)
safety_score = 0.5 + coverage_bonus + total_penalty

# Clamp safety_score to [0, 1]
safety_score = If(safety_score < 0, 0, If(safety_score > 1, 1, safety_score))

# Objective: maximize safety_score
opt.maximize(safety_score)

# ============================================================================
# Check and Output
# ============================================================================

BENCHMARK_MODE = True  # Set False outside benchmark mode
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract prescribed drugs
    prescribed_drugs = []
    for i, drug in enumerate(drugs_data):
        if is_true(model[selected[i]]):
            prescribed_drugs.append({
                "drug_id": drug["drug_id"],
                "dose": model[dose[i]],
                "frequency": model[frequency[i]],
            })
    
    # Extract treated and untreated conditions
    treated_conditions = [cond for cond in patient_conditions if is_true(model[condition_vars[cond]])]
    untreated_conditions = [cond for cond in patient_conditions if cond not in treated_conditions]
    
    # Extract interactions
    detected_interactions = []
    for (d1, d2, sev) in interactions_detected:
        if is_true(model[selected[drugs_data.index(get_drug_by_id(d1))]]) and \
           is_true(model[selected[drugs_data.index(get_drug_by_id(d2))]]):
            detected_interactions.append({
                "drugs": [d1, d2],
                "severity": sev,
            })
    
    # Safety analysis
    safety_analysis = {
        "interactions_detected": detected_interactions,
        "contraindications_avoided": patient_contraindications,
        "safety_score": model.eval(safety_score, model_completion=True),
    }
    
    # Print results
    print("STATUS: sat")
    print("prescribed_drugs:")
    for pd in prescribed_drugs:
        print(f"  - drug_id: {pd['drug_id']}, dose: {pd['dose']}, frequency: {pd['frequency']}")
    print("treated_conditions:", treated_conditions)
    print("untreated_conditions:", untreated_conditions)
    print("safety_analysis:")
    print("  interactions_detected:")
    for ia in detected_interactions:
        print(f"    - drugs: {ia['drugs']}, severity: {ia['severity']}")
    print("  contraindications_avoided:", safety_analysis["contraindications_avoided"])
    print("  safety_score:", safety_analysis["safety_score"])
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")