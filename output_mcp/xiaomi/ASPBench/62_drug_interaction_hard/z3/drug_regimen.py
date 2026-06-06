from z3 import *

# --- Data ---
drugs = {
    'cardio_ease':  {'conditions': ['hypertension'], 'cost': 50,  'toxicity': 20, 'max_dose': 100, 'contraindications': [], 'genetic_contraindications': []},
    'metformax':    {'conditions': ['diabetes'],     'cost': 40,  'toxicity': 25, 'max_dose': 1000, 'contraindications': [], 'genetic_contraindications': []},
    'anxio_calm':   {'conditions': ['anxiety'],      'cost': 70,  'toxicity': 30, 'max_dose': 50,  'contraindications': [], 'genetic_contraindications': []},
    'pain_off':     {'conditions': ['pain'],         'cost': 60,  'toxicity': 15, 'max_dose': 400, 'contraindications': [], 'genetic_contraindications': []},
    'glucopain':    {'conditions': ['diabetes','pain'], 'cost': 110, 'toxicity': 40, 'max_dose': 600, 'contraindications': [], 'genetic_contraindications': ['G6PD_deficiency']},
    'hydro_stress': {'conditions': ['hypertension','anxiety'], 'cost': 90, 'toxicity': 35, 'max_dose': 200, 'contraindications': [], 'genetic_contraindications': []},
    'renal_guard':  {'conditions': ['hypertension'], 'cost': 120, 'toxicity': 10, 'max_dose': 150, 'contraindications': ['renal_failure'], 'genetic_contraindications': []},
    'pain_plus':    {'conditions': ['pain'],         'cost': 80,  'toxicity': 25, 'max_dose': 300, 'contraindications': [], 'genetic_contraindications': []},
}

# Interactions: (drug1, drug2, type, severity, conditional_on)
# Sorted alphabetically for consistency
interactions = [
    ('metformax', 'pain_plus', 'reduced_efficacy', 'moderate', None),
    ('hydro_stress', 'metformax', 'severe_interaction', 'severe', 'diabetes'),
]

patient_conditions = ['hypertension', 'diabetes', 'anxiety', 'pain']
patient_contraindications = ['renal_failure']
patient_genetic = ['G6PD_deficiency']
max_drugs = 4
max_budget = 250
max_toxicity = 100

drug_names = list(drugs.keys())
N = len(drug_names)

# --- Z3 Model ---
solver = Optimize()

# Boolean: is drug prescribed?
prescribed = {d: Bool(f'prescribed_{d}') for d in drug_names}

# Dose (integer, 0 if not prescribed)
dose = {d: Int(f'dose_{d}') for d in drug_names}

for d in drug_names:
    solver.add(dose[d] >= 0)
    solver.add(dose[d] <= drugs[d]['max_dose'])
    # If not prescribed, dose must be 0
    solver.add(Implies(Not(prescribed[d]), dose[d] == 0))
    # If prescribed, dose must be > 0
    solver.add(Implies(prescribed[d], dose[d] > 0))

# 1. Drug limit
solver.add(Sum([If(prescribed[d], 1, 0) for d in drug_names]) <= max_drugs)

# 2. Budget constraint
solver.add(Sum([If(prescribed[d], drugs[d]['cost'], 0) for d in drug_names]) <= max_budget)

# 3. Toxicity constraint
solver.add(Sum([If(prescribed[d], drugs[d]['toxicity'], 0) for d in drug_names]) <= max_toxicity)

# 4. Standard contraindications
for d in drug_names:
    for ci in drugs[d]['contraindications']:
        if ci in patient_contraindications:
            solver.add(Not(prescribed[d]))

# 5. Genetic contraindications
for d in drug_names:
    for gi in drugs[d]['genetic_contraindications']:
        if gi in patient_genetic:
            solver.add(Not(prescribed[d]))

# 6 & 7. Severe interaction prohibition
# hydro_stress + metformax is severe when patient has diabetes (which they do)
solver.add(Not(And(prescribed['hydro_stress'], prescribed['metformax'])))

# 8. Condition coverage
for cond in patient_conditions:
    covering_drugs = [d for d in drug_names if cond in drugs[d]['conditions']]
    solver.add(Or([prescribed[d] for d in covering_drugs]))

# Objective: minimize total cost
total_cost = Sum([If(prescribed[d], drugs[d]['cost'], 0) for d in drug_names])
solver.minimize(total_cost)

# --- Solve ---
result = solver.check()

if result == sat:
    m = solver.model()
    print("STATUS: sat")
    
    # Collect prescribed drugs
    prescribed_list = []
    for d in drug_names:
        if is_true(m.evaluate(prescribed[d])):
            prescribed_list.append(d)
    
    total_cost_val = sum(drugs[d]['cost'] for d in prescribed_list)
    total_tox_val = sum(drugs[d]['toxicity'] for d in prescribed_list)
    
    # Determine treated conditions
    treated = set()
    for d in prescribed_list:
        treated.update(drugs[d]['conditions'])
    untreated = [c for c in patient_conditions if c not in treated]
    
    # Detect interactions among prescribed drugs
    detected_interactions = []
    for (d1, d2, itype, severity, cond) in interactions:
        if d1 in prescribed_list and d2 in prescribed_list:
            if cond is None or cond in patient_conditions:
                pair = tuple(sorted([d1, d2]))
                detected_interactions.append((pair, itype, severity))
    
    print(f"\nPrescribed drugs: {prescribed_list}")
    print(f"Treated conditions: {sorted(treated)}")
    print(f"Untreated conditions: {untreated}")
    print(f"Total cost: {total_cost_val}")
    print(f"Total toxicity: {total_tox_val}")
    print(f"Interactions detected: {detected_interactions}")
    print(f"Contraindications avoided: renal_failure (renal_guard excluded)")
    print(f"Genetic markers respected: G6PD_deficiency (glucopain excluded)")
    
    # Print doses
    for d in prescribed_list:
        print(f"  {d}: dose={m.evaluate(dose[d])}")
    
    print(f"\nExpected minimum cost: 220")
    print(f"Achieved cost: {total_cost_val}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution found.")
else:
    print("STATUS: unknown")