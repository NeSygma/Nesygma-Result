from z3 import *

# Create base solver with all constraints
def get_base_solver():
    solver = Solver()
    F, G, H, K, L, M = Ints('F G H K L M')
    
    # Domain: 0=not assigned, 1=Silva, 2=Thorne
    for p in [F, G, H, K, L, M]:
        solver.add(Or(p == 0, p == 1, p == 2))
    
    # At least 2 photographers at each ceremony
    solver.add(Sum([If(p == 1, 1, 0) for p in [F, G, H, K, L, M]]) >= 2)
    solver.add(Sum([If(p == 2, 1, 0) for p in [F, G, H, K, L, M]]) >= 2)
    
    # Constraint 1: Frost must be assigned together with Heideck (same ceremony, both assigned)
    solver.add(F != 0)
    solver.add(H != 0)
    solver.add(F == H)
    
    # Constraint 2: If Lai and Mays both assigned, different ceremonies
    solver.add(Implies(And(L != 0, M != 0), L != M))
    
    # Constraint 3: If Gonzalez at Silva, Lai at Thorne
    solver.add(Implies(G == 1, L == 2))
    
    # Constraint 4: If Knutson not at Thorne, then Heideck and Mays at Thorne
    solver.add(Implies(K != 2, And(H == 2, M == 2)))
    
    return solver, (F, G, H, K, L, M)

# First, let's verify the base problem has solutions and see one
solver, vars = get_base_solver()
F, G, H, K, L, M = vars
result = solver.check()
print(f"Base problem check result: {result}")
if result == sat:
    m = solver.model()
    names = {F: "Frost", G: "Gonzalez", H: "Heideck", K: "Knutson", L: "Lai", M: "Mays"}
    for var, name in [(F,"Frost"),(G,"Gonzalez"),(H,"Heideck"),(K,"Knutson"),(L,"Lai"),(M,"Mays")]:
        val = m[var].as_long()
        if val == 0:
            print(f"  {name}: NOT assigned")
        elif val == 1:
            print(f"  {name}: Silva")
        else:
            print(f"  {name}: Thorne")
    print()

# Now find which photographers MUST be assigned (mandatory)
# A photographer P is mandatory if there is NO valid solution where P == 0
mandatory = []
for name, var in [("Frost", F), ("Gonzalez", G), ("Heideck", H), ("Knutson", K), ("Lai", L), ("Mays", M)]:
    s2, _ = get_base_solver()
    s2.add(var == 0)  # Check if there's a solution where this photographer is NOT assigned
    if s2.check() == unsat:
        mandatory.append(name)
        print(f"{name} MUST be assigned (mandatory)")
    else:
        print(f"{name} is NOT mandatory")

print(f"\nMandatory set: {mandatory}")

# Now check each option
options = {
    "A": ["Frost", "Heideck"],
    "B": ["Frost", "Heideck", "Knutson"],
    "C": ["Frost", "Heideck", "Knutson", "Lai"],
    "D": ["Frost", "Gonzalez", "Heideck"],
    "E": ["Frost", "Gonzalez", "Heideck", "Mays"]
}

# Map names back
name_to_var = {"Frost": F, "Gonzalez": G, "Heideck": H, "Knutson": K, "Lai": L, "Mays": M}
all_names = ["Frost", "Gonzalez", "Heideck", "Knutson", "Lai", "Mays"]

found_options = []

for letter, opt_list in options.items():
    opt_set = set(opt_list)
    valid = True
    
    # For each photographer in the option: must be mandatory
    for name in opt_set:
        s, _ = get_base_solver()
        s.add(name_to_var[name] == 0)
        if s.check() != unsat:
            # This photographer is NOT mandatory, so this option is wrong
            valid = False
            break
    
    if not valid:
        continue
    
    # For each photographer NOT in the option: must NOT be mandatory
    for name in all_names:
        if name not in opt_set:
            s, _ = get_base_solver()
            s.add(name_to_var[name] == 0)
            if s.check() != sat:
                # This photographer IS mandatory but not in the option, so option is wrong
                valid = False
                break
    
    if valid:
        found_options.append(letter)

if len(found_options) == 1:
    print(f"\nSTATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print(f"\nSTATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print(f"\nSTATUS: unsat")
    print(f"Refine: No options found")