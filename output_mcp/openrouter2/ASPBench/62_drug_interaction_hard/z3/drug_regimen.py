from z3 import *

# Define drug data
# Each drug: id, conditions, cost, toxicity, max_dose, contraindications, genetic_contraindications, interactions
# For simplicity, we encode interactions separately

# Drug list
# id: string
# conditions: list of strings
# cost: int
# toxicity: int
# max_dose: int
# contraindications: list of strings (standard)
# genetic_contraindications: list of strings
# interactions: list of tuples (other_drug_id, type)

# We'll define interactions separately: moderate and severe

# Define drugs

# We'll use a dictionary mapping drug_id to index

# List of drug ids in order
drug_ids = ['cardio_ease', 'metformax', 'anxio_calm', 'pain_off', 'glucopain', 'hydro_stress', 'renal_guard', 'pain_plus']

# Map id to index
id_to_idx = {drug_id: i for i, drug_id in enumerate(drug_ids)}

# Drug attributes
conditions_list = [
    ['hypertension'],  # cardio_ease
    ['diabetes'],      # metformax
    ['anxiety'],       # anxio_calm
    ['pain'],          # pain_off
    ['diabetes', 'pain'],  # glucopain
    ['hypertension', 'anxiety'],  # hydro_stress
    ['hypertension'],  # renal_guard
    ['pain']           # pain_plus
]

costs = [50, 40, 70, 60, 110, 90, 120, 80]

toxicity = [20, 25, 30, 15, 40, 35, 10, 25]

max_doses = [100, 1000, 50, 400, 600, 200, 150, 300]

# Contraindications (standard)
contraindications = [
    [],  # cardio_ease
    [],  # metformax
    [],  # anxio_calm
    [],  # pain_off
    [],  # glucopain
    [],  # hydro_stress
    ['renal_failure'],  # renal_guard
    []   # pain_plus
]

# Genetic contraindications
genetic_contraindications = [
    [],  # cardio_ease
    [],  # metformax
    [],  # anxio_calm
    [],  # pain_off
    ['G6PD_deficiency'],  # glucopain
    [],  # hydro_stress
    [],  # renal_guard
    []   # pain_plus
]

# Interactions: list of tuples (drug1, drug2, type)
# We'll treat interactions as undirected
interactions = [
    ('metformax', 'pain_plus', 'moderate'),
    ('hydro_stress', 'metformax', 'severe')
]

# Patient profile
patient_conditions = ['hypertension', 'diabetes', 'anxiety', 'pain']
patient_contraindications = ['renal_failure']
patient_genetic_markers = ['G6PD_deficiency']
max_drugs = 4
max_budget = 250
max_toxicity = 100

# Solver
opt = Optimize()

# Decision variables: selected (Bool) for each drug
selected = [Bool(f'sel_{drug_id}') for drug_id in drug_ids]

# Dose variables: Int for each drug, equal to max_dose if selected, else 0
# We can compute dose as max_dose * If(selected, 1, 0)
# But we don't need separate variable, we can compute on the fly

# Constraints
# 1. Drug limit
opt.add(Sum([If(sel, 1, 0) for sel in selected]) <= max_drugs)

# 2. Budget constraint
opt.add(Sum([costs[i] * If(selected[i], 1, 0) for i in range(len(drug_ids))]) <= max_budget)

# 3. Toxicity constraint
opt.add(Sum([toxicity[i] * If(selected[i], 1, 0) for i in range(len(drug_ids))]) <= max_toxicity)

# 4. Standard contraindications
for i, cons in enumerate(contraindications):
    for c in cons:
        if c in patient_contraindications:
            opt.add(selected[i] == False)

# 5. Genetic contraindications
for i, gcons in enumerate(genetic_contraindications):
    for g in gcons:
        if g in patient_genetic_markers:
            opt.add(selected[i] == False)

# 6. Severe interaction prohibition
for d1, d2, itype in interactions:
    if itype == 'severe':
        i1 = id_to_idx[d1]
        i2 = id_to_idx[d2]
        opt.add(If(selected[i1], 1, 0) + If(selected[i2], 1, 0) <= 1)

# 7. Condition coverage
for cond in patient_conditions:
    # sum of selected drugs that treat this condition >= 1
    indices = [i for i, conds in enumerate(conditions_list) if cond in conds]
    opt.add(Sum([If(selected[i], 1, 0) for i in indices]) >= 1)

# Objective: minimize total cost
total_cost_expr = Sum([costs[i] * If(selected[i], 1, 0) for i in range(len(drug_ids))])
opt.minimize(total_cost_expr)

# Check
result = opt.check()

if result == sat:
    model = opt.model()
    # Extract selected drugs
    prescribed = []
    for i, sel in enumerate(selected):
        if is_true(model.eval(sel)):
            prescribed.append({'drug_id': drug_ids[i], 'dose': max_doses[i]})
    # Treated conditions
    treated = []
    for cond in patient_conditions:
        # if any selected drug treats cond
        if any(is_true(model.eval(selected[i])) and cond in conditions_list[i] for i in range(len(drug_ids))):
            treated.append(cond)
    untreated = [c for c in patient_conditions if c not in treated]
    # Total cost and toxicity
    total_cost_val = sum(costs[i] for i, sel in enumerate(selected) if is_true(model.eval(sel)))
    total_tox_val = sum(toxicity[i] for i, sel in enumerate(selected) if is_true(model.eval(sel)))
    # Interactions detected
    interactions_detected = []
    for d1, d2, itype in interactions:
        i1 = id_to_idx[d1]
        i2 = id_to_idx[d2]
        if is_true(model.eval(selected[i1])) and is_true(model.eval(selected[i2])):
            # sort drug names alphabetically
            pair = sorted([d1, d2])
            interactions_detected.append(f"{pair[0]} interacts with {pair[1]} ({itype})")
    interactions_detected.sort()
    # Contraindications avoided
    contraindications_avoided = True
    # Genetic markers respected
    genetic_markers_respected = True
    # Print results
    print("STATUS: sat")
    print("prescribed_drugs:", prescribed)
    print("treated_conditions:", treated)
    print("untreated_conditions:", untreated)
    print("total_cost:", total_cost_val)
    print("total_toxicity:", total_tox_val)
    print("safety_analysis:", {
        'interactions_detected': interactions_detected,
        'contraindications_avoided': contraindications_avoided,
        'genetic_markers_respected': genetic_markers_respected
    })
else:
    print("STATUS: unsat")
    if result == unsat:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
    else:
        print("STATUS: unknown")