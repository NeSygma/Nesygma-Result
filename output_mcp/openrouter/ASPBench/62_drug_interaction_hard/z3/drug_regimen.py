from z3 import *

# Define drugs (excluding those contraindicated for the patient)
# Each entry: (name, cost, toxicity, list_of_conditions_treated)
drugs = [
    ('cardio_ease', 50, 20, ['hypertension']),
    ('metformax', 40, 25, ['diabetes']),
    ('anxio_calm', 70, 30, ['anxiety']),
    ('pain_off', 60, 15, ['pain']),
    ('hydro_stress', 90, 35, ['hypertension', 'anxiety']),
    ('pain_plus', 80, 25, ['pain'])
]

# Map drug name to its index for easy lookup
idx = {name: i for i, (name, _, _, _) in enumerate(drugs)}

# Decision variables: whether each drug is selected (Bool)
selected = [Bool(f'sel_{name}') for name, _, _, _ in drugs]

opt = Optimize()

# Constraint 1: at most 4 drugs
opt.add(Sum([If(b, 1, 0) for b in selected]) <= 4)

# Constraint 2: budget <= 250
costs = [cost for _, cost, _, _ in drugs]
opt.add(Sum([If(b, cost, 0) for b, cost in zip(selected, costs)]) <= 250)

# Constraint 3: toxicity <= 100
tox = [t for _, _, t, _ in drugs]
opt.add(Sum([If(b, t, 0) for b, t in zip(selected, tox)]) <= 100)

# Constraint 4: severe interaction prohibition (hydro_stress & metformax)
if 'hydro_stress' in idx and 'metformax' in idx:
    opt.add(Not(And(selected[idx['hydro_stress']], selected[idx['metformax']])))

# Condition coverage: each patient condition must be covered by at least one selected drug
patient_conditions = ['hypertension', 'diabetes', 'anxiety', 'pain']
for cond in patient_conditions:
    covers = []
    for i, (_, _, _, treats) in enumerate(drugs):
        if cond in treats:
            covers.append(selected[i])
    # At least one drug covering the condition must be selected
    opt.add(Or(covers))

# Objective: minimize total cost
total_cost = Sum([If(b, cost, 0) for b, cost in zip(selected, costs)])
opt.minimize(total_cost)

# Solve
if opt.check() == sat:
    m = opt.model()
    # Gather selected drug names
    sel_names = [name for i, (name, _, _, _) in enumerate(drugs) if is_true(m.eval(selected[i]))]
    # Compute totals
    tot_cost = sum(cost for i, (_, cost, _, _) in enumerate(drugs) if is_true(m.eval(selected[i])))
    tot_tox = sum(t for i, (_, _, t, _) in enumerate(drugs) if is_true(m.eval(selected[i])))
    # Treated conditions (union of conditions covered by selected drugs)
    treated = set()
    for i, (_, _, _, treats) in enumerate(drugs):
        if is_true(m.eval(selected[i])):
            treated.update(treats)
    # Interaction detection (known interactions)
    known_interactions = {
        ('metformax', 'pain_plus'): 'moderate',
        ('hydro_stress', 'metformax'): 'severe',
        ('pain_plus', 'anxio_calm'): 'synergy'
    }
    interactions = []
    for (d1, d2), typ in known_interactions.items():
        if d1 in sel_names and d2 in sel_names:
            interactions.append(f"{d1}<->{d2}:{typ}")
    interactions.sort()
    # Output results
    print("STATUS: sat")
    print("selected_drugs =", sel_names)
    print("treated_conditions =", sorted(list(treated)))
    print("total_cost =", tot_cost)
    print("total_toxicity =", tot_tox)
    print("interactions_detected =", interactions)
else:
    print("STATUS: unsat")