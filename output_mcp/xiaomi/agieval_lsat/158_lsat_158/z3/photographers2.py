from z3 import *

# Photographers: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
names = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

# For each photographer: 0 = unassigned, 1 = Silva, 2 = Thorne
assign = [Int(f'assign_{names[i]}') for i in range(6)]

F, G, H, K, L, M = 0, 1, 2, 3, 4, 5

def add_base_constraints(solver):
    # Domain: each assignment is 0, 1, or 2
    for a in assign:
        solver.add(Or(a == 0, a == 1, a == 2))
    
    # At least 2 photographers assigned to Silva
    solver.add(Sum([If(assign[i] == 1, 1, 0) for i in range(6)]) >= 2)
    
    # At least 2 photographers assigned to Thorne
    solver.add(Sum([If(assign[i] == 2, 1, 0) for i in range(6)]) >= 2)
    
    # Constraint 1: Frost must be assigned together with Heideck to one ceremony
    # This means BOTH must be assigned, and to the same ceremony
    solver.add(assign[F] != 0)  # Frost must be assigned
    solver.add(assign[H] != 0)  # Heideck must be assigned
    solver.add(assign[F] == assign[H])  # Same ceremony
    
    # Constraint 2: If Lai and Mays are both assigned, they must be to different ceremonies
    solver.add(Implies(And(assign[L] != 0, assign[M] != 0), assign[L] != assign[M]))
    
    # Constraint 3: If Gonzalez is assigned to Silva, then Lai must be assigned to Thorne
    solver.add(Implies(assign[G] == 1, assign[L] == 2))
    
    # Constraint 4: If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
    solver.add(Implies(assign[K] != 2, And(assign[H] == 2, assign[M] == 2)))

# Check which photographers MUST be assigned
must_be_assigned = []

for i in range(6):
    s = Solver()
    add_base_constraints(s)
    # Try to find a valid assignment where photographer i is NOT assigned
    s.add(assign[i] == 0)
    if s.check() == unsat:
        must_be_assigned.append(names[i])

print("Photographers who must be assigned:", must_be_assigned)

# Also let's find one valid assignment to verify
s = Solver()
add_base_constraints(s)
if s.check() == sat:
    m = s.model()
    print("\nSample valid assignment:")
    for i in range(6):
        val = m[assign[i]]
        if val == 0:
            print(f"  {names[i]}: unassigned")
        elif val == 1:
            print(f"  {names[i]}: Silva")
        else:
            print(f"  {names[i]}: Thorne")

# Evaluate options
must_set = set(must_be_assigned)
options = {
    "A": {"Frost", "Heideck"},
    "B": {"Frost", "Heideck", "Knutson"},
    "C": {"Frost", "Heideck", "Knutson", "Lai"},
    "D": {"Frost", "Gonzalez", "Heideck"},
    "E": {"Frost", "Gonzalez", "Heideck", "Mays"},
}

found_options = []
for letter, opt_set in options.items():
    if opt_set == must_set:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print(f"Refine: No options found. Must-be-assigned set: {must_set}")