from z3 import *

# Define variables for each photographer: 0 = unassigned, 1 = Silva, 2 = Thorne
F, G, H, K, L, M = Ints('F G H K L M')
photographers = [F, G, H, K, L, M]

solver = Solver()

# Base constraints
# 1. Each photographer assigned to at most one ceremony (already by variable domain)
# 2. At least two photographers assigned to each ceremony
solver.add(Sum([If(p == 1, 1, 0) for p in photographers]) >= 2)  # Silva
solver.add(Sum([If(p == 2, 1, 0) for p in photographers]) >= 2)  # Thorne

# 3. Frost and Heideck together: same assignment and both assigned
solver.add(F == H)
solver.add(F != 0)  # both assigned

# 4. If Lai and Mays both assigned, they must be to different ceremonies
solver.add(Implies(And(L != 0, M != 0), L != M))

# 5. If Gonzalez assigned to Silva, then Lai assigned to Thorne
solver.add(Implies(G == 1, L == 2))

# 6. If Knutson not assigned to Thorne, then Heideck and Mays assigned to Thorne
solver.add(Implies(K != 2, And(H == 2, M == 2)))

# Domain constraints: each variable in {0,1,2}
for p in photographers:
    solver.add(Or(p == 0, p == 1, p == 2))

# Answer choices: sets of photographers assigned to Silva University
options = [
    ("A", ["F", "G", "H", "K"]),  # Frost, Gonzalez, Heideck, Knutson
    ("B", ["F", "G", "H"]),       # Frost, Gonzalez, Heideck
    ("C", ["G", "K"]),            # Gonzalez, Knutson
    ("D", ["H", "L"]),            # Heideck, Lai
    ("E", ["K", "M"])             # Knutson, Mays
]

# Map photographer names to variables
var_map = {'F': F, 'G': G, 'H': H, 'K': K, 'L': L, 'M': M}

found_options = []
for letter, silva_set in options:
    solver.push()
    # Add constraints for Silva assignment: exactly these photographers are assigned to Silva (value 1)
    for name, var in var_map.items():
        if name in silva_set:
            solver.add(var == 1)
        else:
            solver.add(var != 1)  # not assigned to Silva (could be 0 or 2)
    # Check satisfiability
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")