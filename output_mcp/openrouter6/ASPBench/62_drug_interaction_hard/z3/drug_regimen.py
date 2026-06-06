from z3 import *

# Define drug IDs and properties
drugs = ["cardio_ease", "metformax", "anxio_calm", "pain_off", "glucopain", "hydro_stress", "renal_guard", "pain_plus"]

# Drug properties: cost, toxicity, max_dose (not used for selection)
costs = {
    "cardio_ease": 50,
    "metformax": 40,
    "anxio_calm": 70,
    "pain_off": 60,
    "glucopain": 110,
    "hydro_stress": 90,
    "renal_guard": 120,
    "pain_plus": 80
}

toxicities = {
    "cardio_ease": 20,
    "metformax": 25,
    "anxio_calm": 30,
    "pain_off": 15,
    "glucopain": 40,
    "hydro_stress": 35,
    "renal_guard": 10,
    "pain_plus": 25
}

# Conditions treated by each drug
conditions_treated = {
    "cardio_ease": ["hypertension"],
    "metformax": ["diabetes"],
    "anxio_calm": ["anxiety"],
    "pain_off": ["pain"],
    "glucopain": ["diabetes", "pain"],
    "hydro_stress": ["hypertension", "anxiety"],
    "renal_guard": ["hypertension"],
    "pain_plus": ["pain"]
}

# Patient conditions
patient_conditions = ["hypertension", "diabetes", "anxiety", "pain"]

# Contraindications
patient_contraindications = ["renal_failure"]
drug_contraindications = {
    "renal_guard": ["renal_failure"]
}

# Genetic markers
patient_genetic_markers = ["G6PD_deficiency"]
drug_genetic_contraindications = {
    "glucopain": ["G6PD_deficiency"]
}

# Interactions
# Format: (drug1, drug2, type, condition_active)
# type: "severe", "moderate", "synergy"
interactions = [
    ("metformax", "pain_plus", "moderate", None),  # always active
    ("hydro_stress", "metformax", "severe", "diabetes"),  # active if patient has diabetes
    ("pain_plus", "anxio_calm", "synergy", "anxiety")  # active if patient has anxiety
]

# Create solver
solver = Optimize()

# Boolean variables for drug selection
select = {drug: Bool(f"select_{drug}") for drug in drugs}

# Add constraint: at most 4 drugs
solver.add(Sum([If(select[drug], 1, 0) for drug in drugs]) <= 4)

# Add constraint: avoid contraindicated drugs
for drug in drugs:
    if drug in drug_contraindications:
        for contraindication in drug_contraindications[drug]:
            if contraindication in patient_contraindications:
                solver.add(Not(select[drug]))

# Add constraint: avoid genetic contraindicated drugs
for drug in drugs:
    if drug in drug_genetic_contraindications:
        for marker in drug_genetic_contraindications[drug]:
            if marker in patient_genetic_markers:
                solver.add(Not(select[drug]))

# Add severe interaction prohibition
for (drug1, drug2, interaction_type, condition) in interactions:
    if interaction_type == "severe":
        if condition is None or condition in patient_conditions:
            # Cannot select both drugs if severe interaction
            solver.add(Not(And(select[drug1], select[drug2])))

# Add condition coverage constraints
for condition in patient_conditions:
    # At least one selected drug must treat this condition
    drugs_treating_condition = [drug for drug in drugs if condition in conditions_treated[drug]]
    solver.add(Or([select[drug] for drug in drugs_treating_condition]))

# Budget constraint: total cost <= 250
total_cost = Sum([If(select[drug], costs[drug], 0) for drug in drugs])
solver.add(total_cost <= 250)

# Toxicity constraint: total toxicity <= 100
total_toxicity = Sum([If(select[drug], toxicities[drug], 0) for drug in drugs])
solver.add(total_toxicity <= 100)

# Objective: minimize total cost
solver.minimize(total_cost)

# Check and get solution
result = solver.check()
print(f"Solver result: {result}")

if result == sat:
    model = solver.model()
    print("STATUS: sat")
    
    # Get selected drugs
    selected_drugs = [drug for drug in drugs if is_true(model[select[drug]])]
    print(f"Selected drugs: {selected_drugs}")
    
    # Calculate totals
    total_cost_val = sum(costs[drug] for drug in selected_drugs)
    total_toxicity_val = sum(toxicities[drug] for drug in selected_drugs)
    
    # Determine treated conditions
    treated_conditions = set()
    for drug in selected_drugs:
        for cond in conditions_treated[drug]:
            treated_conditions.add(cond)
    untreated_conditions = [cond for cond in patient_conditions if cond not in treated_conditions]
    
    # Detect interactions
    interactions_detected = []
    for (drug1, drug2, interaction_type, condition) in interactions:
        if drug1 in selected_drugs and drug2 in selected_drugs:
            if condition is None or condition in patient_conditions:
                # Sort drugs alphabetically
                sorted_drugs = sorted([drug1, drug2])
                interaction_desc = f"{sorted_drugs[0]}_{sorted_drugs[1]}_{interaction_type}"
                interactions_detected.append(interaction_desc)
    
    # Contraindications avoided
    contraindications_avoided = patient_contraindications[:]
    
    # Genetic markers respected
    genetic_markers_respected = patient_genetic_markers[:]
    
    # Print results in required format
    print(f"prescribed_drugs: {[{'drug_id': drug, 'dose': 'max'} for drug in selected_drugs]}")
    print(f"treated_conditions: {list(treated_conditions)}")
    print(f"untreated_conditions: {untreated_conditions}")
    print(f"total_cost: {total_cost_val}")
    print(f"total_toxicity: {total_toxicity_val}")
    print(f"safety_analysis:")
    print(f"  interactions_detected: {interactions_detected}")
    print(f"  contraindications_avoided: {contraindications_avoided}")
    print(f"  genetic_markers_respected: {genetic_markers_respected}")
    
    # Verify expected minimum cost
    if total_cost_val == 220:
        print(f"Expected minimum cost achieved: {total_cost_val}")
    else:
        print(f"Note: Found cost {total_cost_val}, expected 220")
        
elif result == unsat:
    print("STATUS: unsat")
    print("No solution exists satisfying all constraints")
else:
    print("STATUS: unknown")
    print("Solver returned unknown result")