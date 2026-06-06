from z3 import *

# ============================================================
# DRUG REGIMEN OPTIMIZATION
# ============================================================

# Available Drugs
drugs = ["cardio_ease", "metformax", "anxio_calm", "pain_off", "glucopain", "hydro_stress", "renal_guard", "pain_plus"]
N = len(drugs)

# Drug properties
cost = {
    "cardio_ease": 50,
    "metformax": 40,
    "anxio_calm": 70,
    "pain_off": 60,
    "glucopain": 110,
    "hydro_stress": 90,
    "renal_guard": 120,
    "pain_plus": 80
}

toxicity = {
    "cardio_ease": 20,
    "metformax": 25,
    "anxio_calm": 30,
    "pain_off": 15,
    "glucopain": 40,
    "hydro_stress": 35,
    "renal_guard": 10,
    "pain_plus": 25
}

max_dose = {
    "cardio_ease": 100,
    "metformax": 1000,
    "anxio_calm": 50,
    "pain_off": 400,
    "glucopain": 600,
    "hydro_stress": 200,
    "renal_guard": 150,
    "pain_plus": 300
}

# Conditions each drug treats
treats = {
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
contraindicated = {
    "renal_guard": ["renal_failure"]
}

# Genetic contraindications
genetic_contraindicated = {
    "glucopain": ["G6PD_deficiency"]
}

# Patient info
patient_contraindications = ["renal_failure"]
patient_genetic_markers = ["G6PD_deficiency"]

# Interactions
# metformax interacts with pain_plus (reduced_efficacy, moderate)
# hydro_stress has severe interaction with metformax if patient has diabetes
# pain_plus synergy with anxio_calm for anxiety (efficacy_bonus=2)

# ============================================================
# DECISION VARIABLES
# ============================================================

# Binary: is drug selected?
selected = [Bool(f"selected_{d}") for d in drugs]

# Dose for each drug (if selected, dose > 0; if not selected, dose = 0)
dose = [Real(f"dose_{d}") for d in drugs]

opt = Optimize()

# ============================================================
# CONSTRAINTS
# ============================================================

# Dose bounds: if selected, dose in (0, max_dose]; if not selected, dose = 0
for i in range(N):
    opt.add(Implies(selected[i], dose[i] > 0))
    opt.add(Implies(selected[i], dose[i] <= max_dose[drugs[i]]))
    opt.add(Implies(Not(selected[i]), dose[i] == 0))

# 1. Drug limit: at most 4 drugs
opt.add(Sum([If(selected[i], 1, 0) for i in range(N)]) <= 4)

# 2. Budget constraint: total cost <= 250
total_cost = Sum([If(selected[i], cost[drugs[i]], 0) for i in range(N)])
opt.add(total_cost <= 250)

# 3. Toxicity constraint: total toxicity <= 100
total_toxicity = Sum([If(selected[i], toxicity[drugs[i]], 0) for i in range(N)])
opt.add(total_toxicity <= 100)

# 4. Standard contraindications: avoid drugs contraindicated with patient's conditions
for i in range(N):
    d = drugs[i]
    if d in contraindicated:
        for cond in contraindicated[d]:
            if cond in patient_contraindications:
                opt.add(Not(selected[i]))

# 5. Genetic contraindications: avoid drugs contraindicated with patient's genetic markers
for i in range(N):
    d = drugs[i]
    if d in genetic_contraindicated:
        for marker in genetic_contraindicated[d]:
            if marker in patient_genetic_markers:
                opt.add(Not(selected[i]))

# 6 & 7. Interaction detection and severe interaction prohibition
# hydro_stress has severe interaction with metformax if patient has diabetes
# Patient HAS diabetes, so this is a severe interaction -> cannot prescribe both
idx_hydro = drugs.index("hydro_stress")
idx_met = drugs.index("metformax")
opt.add(Not(And(selected[idx_hydro], selected[idx_met])))

# metformax interacts with pain_plus (reduced_efficacy, moderate) - moderate, not severe, so allowed
# pain_plus synergy with anxio_calm - beneficial, not prohibited

# 8. Condition coverage: treat all patient conditions
for cond in patient_conditions:
    # At least one selected drug must treat this condition
    opt.add(Or([And(selected[i], cond in treats[drugs[i]]) for i in range(N)]))

# ============================================================
# OBJECTIVE: Minimize total cost
# ============================================================
opt.minimize(total_cost)

# ============================================================
# SOLVE
# ============================================================
result = opt.check()

if result == sat:
    m = opt.model()
    print("STATUS: sat")
    print("Optimal solution found!")
    print()
    
    prescribed = []
    for i in range(N):
        if is_true(m[selected[i]]):
            d = drugs[i]
            d_val = m[dose[i]]
            prescribed.append((d, d_val))
            print(f"  {d}: dose = {d_val}")
    
    print()
    print(f"Total cost: {sum(cost[d] for d, _ in prescribed)}")
    print(f"Total toxicity: {sum(toxicity[d] for d, _ in prescribed)}")
    print(f"Number of drugs: {len(prescribed)}")
    
    # Treated conditions
    treated = set()
    for d, _ in prescribed:
        for c in treats[d]:
            treated.add(c)
    print(f"Treated conditions: {sorted(treated)}")
    untreated = [c for c in patient_conditions if c not in treated]
    print(f"Untreated conditions: {untreated}")
    
    # Safety analysis
    print()
    print("Safety Analysis:")
    print(f"  Contraindications avoided: {patient_contraindications}")
    print(f"  Genetic markers respected: {patient_genetic_markers}")
    
    # Interactions detected
    interactions = []
    drug_names = [d for d, _ in prescribed]
    if "metformax" in drug_names and "pain_plus" in drug_names:
        interactions.append(("metformax", "pain_plus", "reduced_efficacy", "moderate"))
    if "hydro_stress" in drug_names and "metformax" in drug_names:
        interactions.append(("hydro_stress", "metformax", "severe"))
    if "pain_plus" in drug_names and "anxio_calm" in drug_names:
        interactions.append(("anxio_calm", "pain_plus", "synergy", "efficacy_bonus=2"))
    
    if interactions:
        print("  Interactions detected:")
        for inter in interactions:
            print(f"    - {inter}")
    else:
        print("  Interactions detected: None")
    
    print()
    print(f"Expected minimum cost: 220")
    print(f"Achieved cost: {sum(cost[d] for d, _ in prescribed)}")
    
elif result == unsat:
    print("STATUS: unsat")
    print("No feasible solution exists.")
else:
    print("STATUS: unknown")