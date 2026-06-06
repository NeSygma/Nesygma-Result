from z3 import *

# ============================================================================
# Problem: Pharmaceutical Safety - Optimal Drug Prescription
# ============================================================================

# Patient data
patient_conditions = ['pain', 'hypertension', 'diabetes']
patient_contraindications = ['bleeding_disorder']
max_drugs = 3

# Drug data (using drug IDs as keys)
drugs_data = {
    'drug1': {
        'treats': ['pain', 'inflammation'],
        'contraindicates': ['bleeding_disorder'],
        'max_dose': 4000,
        'interactions': [('drug2', 'moderate')]
    },
    'drug2': {
        'treats': ['blood_clot_prevention'],
        'contraindicates': ['pregnancy'],
        'max_dose': 10,
        'interactions': [('drug1', 'moderate')]
    },
    'drug3': {
        'treats': ['hypertension'],
        'contraindicates': ['kidney_disease'],
        'max_dose': 40,
        'interactions': [('drug4', 'mild'), ('drug5', 'moderate')]
    },
    'drug4': {
        'treats': ['diabetes'],
        'contraindicates': ['kidney_disease'],
        'max_dose': 2000,
        'interactions': [('drug3', 'mild')]
    },
    'drug5': {
        'treats': ['pain', 'inflammation'],
        'contraindicates': [],
        'max_dose': 2400,
        'interactions': [('drug3', 'moderate')]
    }
}

# Create solver
solver = Solver()

# Decision variables
# Which drugs are prescribed
prescribed = {drug_id: Bool(f'prescribed_{drug_id}') for drug_id in drugs_data}

# Doses for prescribed drugs (only relevant if drug is prescribed)
doses = {drug_id: Int(f'dose_{drug_id}') for drug_id in drugs_data}

# Which conditions are treated
treated = {cond: Bool(f'treated_{cond}') for cond in patient_conditions}

# ============================================================================
# Add constraints
# ============================================================================

# 1. Maximum drugs constraint
solver.add(Sum([If(prescribed[drug_id], 1, 0) for drug_id in drugs_data]) <= max_drugs)

# 2. Contraindications constraint
# Cannot prescribe drugs that have contraindications matching patient's
for drug_id, data in drugs_data.items():
    for contra in data['contraindicates']:
        if contra in patient_contraindications:
            solver.add(Not(prescribed[drug_id]))

# 3. Dose constraints
for drug_id, data in drugs_data.items():
    solver.add(If(prescribed[drug_id],
                  And(doses[drug_id] >= 1, doses[drug_id] <= data['max_dose']),
                  doses[drug_id] == 0))

# 4. Condition treatment constraints
# A condition is treated if at least one prescribed drug treats it
for cond in patient_conditions:
    # Get drugs that treat this condition
    treating_drugs = [drug_id for drug_id, data in drugs_data.items() if cond in data['treats']]
    
    # If at least one treating drug is prescribed, the condition is treated
    solver.add(Implies(Or([prescribed[d] for d in treating_drugs]),
                       treated[cond]))
    
    # If none of the treating drugs are prescribed, the condition is not treated
    solver.add(Implies(Not(Or([prescribed[d] for d in treating_drugs])),
                       Not(treated[cond])))

# 5. Interaction penalties
# Helper function to get penalty value from severity
def get_penalty(severity):
    if severity == 'severe':
        return 0.3
    elif severity == 'moderate':
        return 0.15
    elif severity == 'mild':
        return 0.05
    else:
        return 0.0

# Calculate total penalty as a Real
total_penalty = Real('total_penalty')
interaction_terms = []

# For each pair of drugs, check if they have interactions and both are prescribed
drug_list = list(drugs_data.keys())
for i in range(len(drug_list)):
    for j in range(i+1, len(drug_list)):
        drug_id1, drug_id2 = drug_list[i], drug_list[j]
        
        # Check if both drugs are prescribed
        both_prescribed = And(prescribed[drug_id1], prescribed[drug_id2])
        
        # Find interactions between these two drugs
        interactions = []
        for (other_id, severity) in drugs_data[drug_id1]['interactions']:
            if other_id == drug_id2:
                interactions.append((other_id, severity))
        for (other_id, severity) in drugs_data[drug_id2]['interactions']:
            if other_id == drug_id1:
                interactions.append((other_id, severity))
        
        # For each interaction, add penalty if both drugs are prescribed
        for (other_id, severity) in interactions:
            penalty = get_penalty(severity)
            interaction_terms.append(If(both_prescribed, penalty, 0.0))

# Sum all penalties
if interaction_terms:
    solver.add(total_penalty == Sum(interaction_terms))
else:
    solver.add(total_penalty == 0.0)

# 6. Safety score calculation
total_conditions = len(patient_conditions)
treated_count = Sum([If(treated[cond], 1, 0) for cond in patient_conditions])
coverage_bonus = (to_real(treated_count) / total_conditions) * 0.5
safety_score = 0.5 + coverage_bonus - total_penalty
solver.add(safety_score >= 0.0, safety_score <= 1.0)

# ============================================================================
# Optimization
# ============================================================================
opt = Optimize()
opt.add(solver.assertions())
opt.maximize(safety_score)

# ============================================================================
# Check and extract model
# ============================================================================
result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract prescribed drugs
    prescribed_drugs = []
    for drug_id in drugs_data:
        if is_true(model[prescribed[drug_id]]):
            dose_val = model[doses[drug_id]]
            prescribed_drugs.append({
                'drug_id': drug_id,
                'dose': dose_val,
                'frequency': 'as directed'  # Simplified for this model
            })
    
    # Extract treated conditions
    treated_conditions = [cond for cond in patient_conditions if is_true(model[treated[cond]])]
    untreated_conditions = [cond for cond in patient_conditions if cond not in treated_conditions]
    
    # Extract interactions
    interactions_detected = []
    for i in range(len(drug_list)):
        for j in range(i+1, len(drug_list)):
            drug_id1, drug_id2 = drug_list[i], drug_list[j]
            if is_true(model[prescribed[drug_id1]]) and is_true(model[prescribed[drug_id2]]):
                # Check if they have interactions
                for (other_id, severity) in drugs_data[drug_id1]['interactions']:
                    if other_id == drug_id2:
                        interactions_detected.append({
                            'drugs': [drug_id1, drug_id2],
                            'severity': severity
                        })
                for (other_id, severity) in drugs_data[drug_id2]['interactions']:
                    if other_id == drug_id1:
                        # Avoid duplicates
                        if not any(set(inter['drugs']) == {drug_id1, drug_id2} for inter in interactions_detected):
                            interactions_detected.append({
                                'drugs': [drug_id2, drug_id1],
                                'severity': severity
                            })
    
    # Safety analysis
    contraindications_avoided = patient_contraindications  # Informational
    
    # Calculate safety score from model
    safety_score_val = model.eval(safety_score)
    
    # Print results
    print("STATUS: sat")
    print("\n=== Prescription Details ===")
    print("Prescribed drugs:")
    for drug in prescribed_drugs:
        print(f"  - drug_id: {drug['drug_id']}, dose: {drug['dose']} mg, frequency: {drug['frequency']}")
    
    print("\nTreated conditions:", treated_conditions)
    print("Untreated conditions:", untreated_conditions)
    
    print("\n=== Safety Analysis ===")
    print("Contraindications avoided:", contraindications_avoided)
    print("Interactions detected:")
    if interactions_detected:
        for inter in interactions_detected:
            print(f"  - drugs: {inter['drugs']}, severity: {inter['severity']}")
    else:
        print("  None")
    
    print("\nSafety score:", safety_score_val)
    
elif result == unsat:
    print("STATUS: unsat")
    print("RAW_RESULT: unsat")
else:
    print("STATUS: unknown")