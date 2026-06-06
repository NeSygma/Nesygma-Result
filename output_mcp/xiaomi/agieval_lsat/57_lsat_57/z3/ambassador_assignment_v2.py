from z3 import *

solver = Solver()

# Countries: Venezuela=0, Yemen=1, Zambia=2
# Candidates: Jaramillo=0, Kayne=1, Landon=2, Novetzke=3, Ong=4
candidates = ['Jaramillo', 'Kayne', 'Landon', 'Novetzke', 'Ong']
countries = ['Venezuela', 'Yemen', 'Zambia']

# Assignment variables: assign[c] = candidate assigned to country c
assign = [Int(f'assign_{c}') for c in range(3)]

# Each assignment is a valid candidate (0-4)
for c in range(3):
    solver.add(assign[c] >= 0, assign[c] <= 4)

# All assignments are distinct (no ambassador assigned to more than one country)
solver.add(Distinct(assign))

# Constraint 1: Either Kayne(1) or Novetzke(3), but not both, is assigned
kayne_assigned = Or([assign[c] == 1 for c in range(3)])
novetzke_assigned = Or([assign[c] == 3 for c in range(3)])
solver.add(Xor(kayne_assigned, novetzke_assigned))

# Constraint 2: If Jaramillo(0) is assigned, then Kayne(1) is assigned
jaramillo_assigned = Or([assign[c] == 0 for c in range(3)])
solver.add(Implies(jaramillo_assigned, kayne_assigned))

# Constraint 3: If Ong(4) is assigned to Venezuela(0), then Kayne(1) is not assigned to Yemen(1)
solver.add(Implies(assign[0] == 4, assign[1] != 1))

# Constraint 4: If Landon(2) is assigned, it is to Zambia(2)
landon_assigned = Or([assign[c] == 2 for c in range(3)])
solver.add(Implies(landon_assigned, assign[2] == 2))

# Additional constraint from the question: Kayne is assigned to Yemen
solver.add(assign[1] == 1)

# First, let's see what the base constraints imply
print("=== Checking base constraints ===")
if solver.check() == sat:
    m = solver.model()
    print("Base model found:")
    for c in range(3):
        cand = m[assign[c]].as_long()
        print(f"  {countries[c]}: {candidates[cand]}")
else:
    print("Base constraints are unsatisfiable!")

# Now check which options MUST be true (i.e., are entailed by the constraints)
# An option "must be true" if adding its negation makes the problem unsatisfiable

options = {
    "A": "Jaramillo is assigned as ambassador to Venezuela.",
    "B": "Landon is assigned as ambassador to Zambia.",
    "C": "Ong is assigned as ambassador to Zambia.",
    "D": "Jaramillo is not assigned to an ambassadorship.",
    "E": "Ong is not assigned to an ambassadorship."
}

opt_constrs = {
    "A": (assign[0] == 0),  # Jaramillo to Venezuela
    "B": (assign[2] == 2),  # Landon to Zambia
    "C": (assign[2] == 4),  # Ong to Zambia
    "D": Not(jaramillo_assigned),  # Jaramillo not assigned
    "E": Not(Or([assign[c] == 4 for c in range(3)]))  # Ong not assigned
}

print("\n=== Checking which options MUST be true ===")
must_be_true = []
for letter, constr in opt_constrs.items():
    s = Solver()
    # Add all base constraints
    s.add(assign[0] >= 0, assign[0] <= 4)
    s.add(assign[1] >= 0, assign[1] <= 4)
    s.add(assign[2] >= 0, assign[2] <= 4)
    s.add(Distinct(assign))
    s.add(Xor(kayne_assigned, novetzke_assigned))
    s.add(Implies(jaramillo_assigned, kayne_assigned))
    s.add(Implies(assign[0] == 4, assign[1] != 1))
    s.add(Implies(landon_assigned, assign[2] == 2))
    s.add(assign[1] == 1)
    
    # Add the NEGATION of the option
    s.add(Not(constr))
    
    result = s.check()
    if result == unsat:
        # The negation is unsatisfiable, so the option MUST be true
        must_be_true.append(letter)
        print(f"  {letter}: MUST be true (negation is unsat)")
    else:
        print(f"  {letter}: NOT necessarily true (negation is sat)")

print(f"\nOptions that must be true: {must_be_true}")

if len(must_be_true) == 1:
    print("STATUS: sat")
    print(f"answer:{must_be_true[0]}")
elif len(must_be_true) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options must be true {must_be_true}")
else:
    print("STATUS: unsat")
    print("Refine: No options must be true")