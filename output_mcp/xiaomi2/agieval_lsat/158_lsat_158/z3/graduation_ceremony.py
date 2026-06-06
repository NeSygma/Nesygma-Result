from z3 import *

# Photographers: 0=Frost, 1=Gonzalez, 2=Heideck, 3=Knutson, 4=Lai, 5=Mays
# Ceremonies: 0=unassigned, 1=Silva, 2=Thorne
names = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

def make_base_solver():
    """Create a solver with all base constraints."""
    s = Solver()
    
    # Assignment variables: 0=unassigned, 1=Silva, 2=Thorne
    assign = [Int(f'assign_{names[i]}') for i in range(6)]
    
    for a in assign:
        s.add(Or(a == 0, a == 1, a == 2))
    
    F, G, H, K, L, M = assign  # Frost, Gonzalez, Heideck, Knutson, Lai, Mays
    
    # Constraint 1: Frost must be assigned together with Heideck to one ceremony
    # Both must be assigned and at the same ceremony
    s.add(F != 0)  # Frost must be assigned
    s.add(H != 0)  # Heideck must be assigned
    s.add(F == H)   # Same ceremony
    
    # Constraint 2: If Lai and Mays are both assigned, different ceremonies
    s.add(Implies(And(L != 0, M != 0), L != M))
    
    # Constraint 3: If Gonzalez at Silva, then Lai at Thorne
    s.add(Implies(G == 1, L == 2))
    
    # Constraint 4: If Knutson not at Thorne, then Heideck and Mays at Thorne
    s.add(Implies(K != 2, And(H == 2, M == 2)))
    
    # Each ceremony must have at least 2 photographers
    silva_count = Sum([If(a == 1, 1, 0) for a in assign])
    thorne_count = Sum([If(a == 2, 1, 0) for a in assign])
    s.add(silva_count >= 2)
    s.add(thorne_count >= 2)
    
    return s, assign

# For each photographer, check if there exists a valid config where they are NOT assigned
must_be_assigned = []
for i in range(6):
    s, assign = make_base_solver()
    s.add(assign[i] == 0)  # Force this photographer to be unassigned
    result = s.check()
    if result == unsat:
        # No valid config without this photographer -> must be assigned
        must_be_assigned.append(names[i])
    elif result == sat:
        pass  # Can be unassigned
    else:
        print(f"Unknown for {names[i]}")

print(f"Photographers who MUST be assigned: {must_be_assigned}")

# Now check each answer option
# Option A: Frost, Heideck
# Option B: Frost, Heideck, Knutson
# Option C: Frost, Heideck, Knutson, Lai
# Option D: Frost, Gonzalez, Heideck
# Option E: Frost, Gonzalez, Heideck, Mays

options = {
    "A": ["Frost", "Heideck"],
    "B": ["Frost", "Heideck", "Knutson"],
    "C": ["Frost", "Heideck", "Knutson", "Lai"],
    "D": ["Frost", "Gonzalez", "Heideck"],
    "E": ["Frost", "Gonzalez", "Heideck", "Mays"],
}

# The correct option must exactly match the set of must-be-assigned photographers
must_set = set(must_be_assigned)
found_options = []
for letter, members in options.items():
    if set(members) == must_set:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")