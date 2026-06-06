from z3 import *

# ============================================================================
# Problem: Optimal Drug Regimen Design with Constraints
# ============================================================================

# BENCHMARK_MODE: ON (problem is guaranteed solvable)
BENCHMARK_MODE = True

# ============================================================================
# 1. Declare symbolic variables and data structures
# ============================================================================

# Decision variables: whether to prescribe each drug and its dose
# Drugs: CardioEase, Metformax, AnxioCalm, PainOff, Glucopain, HydroStress, RenalGuard, PainPlus
prescribed = [Bool(f'prescribed_{drug}') for drug in [
    'cardio_ease', 'metformax', 'anxio_calm', 'pain_off', 
    'glucopain', 'hydro_stress', 'renal_guard', 'pain_plus'
]]

doses = [Int(f'dose_{drug}') for drug in [
    'cardio_ease', 'metformax', 'anxio_calm', 'pain_off', 
    'glucopain', 'hydro_stress', 'renal_guard', 'pain_plus'
]]

# ============================================================================
# 2. Drug and patient data
# ============================================================================

# Drug properties: (cost, toxicity, max_dose, conditions_treated, contraindications, genetic_contraindications, interactions)
drug_data = {
    'cardio_ease': (50, 20, 100, ['hypertension'], [], [], []),
    'metformax': (40, 25, 1000, ['diabetes'], [], [], [('pain_plus', 'reduced_efficacy', 'moderate')]),
    'anxio_calm': (70, 30, 50, ['anxiety'], [], [], [('pain_plus', 'synergy', 'anxiety')]),
    'pain_off': (60, 15, 400, ['pain'], [], [], []),
    'glucopain': (110, 40, 600, ['diabetes', 'pain'], ['G6PD_deficiency'], ['G6PD_deficiency'], []),
    'hydro_stress': (90, 35, 200, ['hypertension', 'anxiety'], [], [], [('metformax', 'severe_interaction', 'diabetes')]),
    'renal_guard': (120, 10, 150, ['hypertension'], ['renal_failure'], [], []),
    'pain_plus': (80, 25, 300, ['pain'], [], [], [('metformax', 'reduced_efficacy', 'moderate'), ('anxio_calm', 'synergy', 'anxiety')]),
}

# Patient profile
patient_conditions = ['hypertension', 'diabetes', 'anxiety', 'pain']
patient_contraindications = ['renal_failure']
patient_genetic_markers = ['G6PD_deficiency']

# ============================================================================
# 3. Constraints
# ============================================================================

solver = Solver()

# 3.1 Drug limit: at most 4 drugs
solver.add(Sum(prescribed) <= 4)

# 3.2 Dose bounds: 0 <= dose <= max_dose for each drug
for i, drug in enumerate(drug_data.keys()):
    max_dose = drug_data[drug][2]
    solver.add(doses[i] >= 0)
    solver.add(doses[i] <= max_dose)

# 3.3 Budget constraint: total cost <= 250
costs = [drug_data[drug][0] for drug in drug_data.keys()]
total_cost = Sum([If(prescribed[i], costs[i], 0) for i in range(len(prescribed))])
solver.add(total_cost <= 250)

# 3.4 Toxicity constraint: total toxicity <= 100
toxicities = [drug_data[drug][1] for drug in drug_data.keys()]
total_toxicity = Sum([If(prescribed[i], toxicities[i], 0) for i in range(len(prescribed))])
solver.add(total_toxicity <= 100)

# 3.5 Standard contraindications: avoid drugs with contraindications matching patient
for i, drug in enumerate(drug_data.keys()):
    contraindications = drug_data[drug][4]
    # If drug has any contraindication that matches patient's, it cannot be prescribed
    solver.add(Not(And(prescribed[i], Or([c == pc for c in contraindications for pc in patient_contraindications]))))

# 3.6 Genetic contraindications: avoid drugs with genetic contraindications matching patient genetic markers
for i, drug in enumerate(drug_data.keys()):
    genetic_contraindications = drug_data[drug][5]
    solver.add(Not(And(prescribed[i], Or([g == pg for g in genetic_contraindications for pg in patient_genetic_markers]))))

# 3.7 Condition coverage: all patient conditions must be treated
# For each condition, at least one prescribed drug must treat it
for cond in patient_conditions:
    drugs_treating_cond = [
        prescribed[i] for i, drug in enumerate(drug_data.keys()) 
        if cond in drug_data[drug][3]
    ]
    solver.add(Or(drugs_treating_cond))

# 3.8 Interaction detection and prohibition
# We will collect all interactions and ensure no severe interactions are active
# Also, for moderate/reduced efficacy, we will not prohibit but note them

# Helper: get index of a drug by name
name_to_idx = {name: i for i, name in enumerate(drug_data.keys())}

# Collect all interactions (drug1, drug2, type, condition_trigger)
# We will ensure no severe interactions are active
severe_interactions = []
moderate_interactions = []
synergy_interactions = []

for drug in drug_data.keys():
    for (other, itype, trigger) in drug_data[drug][6]:
        i1 = name_to_idx[drug]
        i2 = name_to_idx[other]
        if itype == 'severe_interaction':
            severe_interactions.append((i1, i2, trigger))
        elif itype == 'reduced_efficacy':
            moderate_interactions.append((i1, i2, trigger))
        elif itype == 'synergy':
            synergy_interactions.append((i1, i2, trigger))

# Prohibit severe interactions: cannot prescribe both drugs in a severe interaction
for (i1, i2, trigger) in severe_interactions:
    # Severe interaction is only active if the trigger condition is present in the patient
    # Here, trigger is a condition (e.g., 'diabetes')
    # We assume the condition is present if the patient has it (which they do)
    solver.add(Not(And(prescribed[i1], prescribed[i2])))

# Note: moderate interactions and synergies are allowed but noted in safety analysis

# ============================================================================
# 4. Objective: minimize total cost
# ============================================================================

# Use Optimize to minimize cost
opt = Optimize()

# Copy all constraints from solver to opt
for c in solver.assertions():
    opt.add(c)

# Minimize total cost
opt.minimize(total_cost)

# ============================================================================
# 5. Solve and output
# ============================================================================

result = opt.check()

if result == sat:
    model = opt.model()
    
    # Extract prescribed drugs and doses
    prescribed_drugs = []
    for i, drug in enumerate(drug_data.keys()):
        if is_true(model[prescribed[i]]):
            prescribed_drugs.append((drug, model[doses[i]]))
    
    # Calculate total cost and toxicity
    total_cost_val = sum(drug_data[drug][0] for drug, _ in prescribed_drugs)
    total_toxicity_val = sum(drug_data[drug][1] for drug, _ in prescribed_drugs)
    
    # Treated conditions
    treated_conditions = set()
    for drug, _ in prescribed_drugs:
        for cond in drug_data[drug][3]:
            treated_conditions.add(cond)
    untreated_conditions = [cond for cond in patient_conditions if cond not in treated_conditions]
    
    # Safety analysis: interactions detected
    interactions_detected = []
    for (i1, i2, trigger) in moderate_interactions + synergy_interactions:
        if is_true(model[prescribed[i1]]) and is_true(model[prescribed[i2]]):
            drug1 = list(drug_data.keys())[i1]
            drug2 = list(drug_data.keys())[i2]
            interactions_detected.append((drug1, drug2, trigger))
    
    # Sort interactions_detected alphabetically by drug names
    interactions_detected.sort(key=lambda x: (x[0], x[1]))
    
    # Contraindications avoided and genetic markers respected are guaranteed by constraints
    
    print("STATUS: sat")
    print("prescribed_drugs:")
    for drug, dose in prescribed_drugs:
        print(f"  - drug_id: {drug}, dose: {dose}")
    print(f"total_cost: {total_cost_val}")
    print(f"total_toxicity: {total_toxicity_val}")
    print("treated_conditions:", sorted(list(treated_conditions)))
    print("untreated_conditions:", untreated_conditions)
    print("safety_analysis:")
    print("  interactions_detected:")
    for (d1, d2, t) in interactions_detected:
        print(f"    - drugs: [{d1}, {d2}], type: {t}")
    print("  contraindications_avoided: True")
    print("  genetic_markers_respected: True")
    
elif result == unsat:
    print("STATUS: unsat")
    if BENCHMARK_MODE:
        print("RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)")
else:
    print("STATUS: unknown")