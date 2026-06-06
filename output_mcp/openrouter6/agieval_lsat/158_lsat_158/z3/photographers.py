from z3 import *

# Define variables
F, G, H, K, L, M = Ints('F G H K L M')

# Domain constraints: 0 = unassigned, 1 = Silva, 2 = Thorne
solver = Solver()
for var in [F, G, H, K, L, M]:
    solver.add(var >= 0, var <= 2)

# At least two assigned to Silva
silva_count = Sum([If(var == 1, 1, 0) for var in [F, G, H, K, L, M]])
solver.add(silva_count >= 2)

# At least two assigned to Thorne
thorne_count = Sum([If(var == 2, 1, 0) for var in [F, G, H, K, L, M]])
solver.add(thorne_count >= 2)

# Frost and Heideck together
solver.add(F == H)
solver.add(F != 0)  # both assigned

# If Lai and Mays both assigned, different ceremonies
solver.add(Implies(And(L != 0, M != 0), L != M))

# If Gonzalez assigned to Silva, then Lai to Thorne
solver.add(Implies(G == 1, L == 2))

# If Knutson not assigned to Thorne, then Heideck and Mays assigned to Thorne
solver.add(Implies(K != 2, And(H == 2, M == 2)))

# Check base satisfiability
print("Checking base satisfiability...")
result = solver.check()
if result == sat:
    print("Base problem is satisfiable.")
    m = solver.model()
    print("Example assignment:")
    for var in [F, G, H, K, L, M]:
        val = m[var]
        if val == 0:
            status = "unassigned"
        elif val == 1:
            status = "Silva"
        else:
            status = "Thorne"
        print(f"{var}: {status}")
else:
    print("Base problem is unsatisfiable. Something wrong.")
    exit()

# Determine forced photographers: those that cannot be unassigned
forced = []
photographers = [('Frost', F), ('Gonzalez', G), ('Heideck', H), ('Knutson', K), ('Lai', L), ('Mays', M)]
for name, var in photographers:
    s = Solver()
    # Add all base constraints
    for v in [F, G, H, K, L, M]:
        s.add(v >= 0, v <= 2)
    s.add(silva_count >= 2)
    s.add(thorne_count >= 2)
    s.add(F == H)
    s.add(F != 0)
    s.add(Implies(And(L != 0, M != 0), L != M))
    s.add(Implies(G == 1, L == 2))
    s.add(Implies(K != 2, And(H == 2, M == 2)))
    # Add constraint that this photographer is unassigned
    s.add(var == 0)
    res = s.check()
    if res == unsat:
        forced.append(name)
        print(f"{name} must be assigned (cannot be unassigned).")
    else:
        print(f"{name} can be unassigned (there exists a solution where they are unassigned).")

print("\nForced photographers:", forced)

# Now compare with options
options = {
    'A': ['Frost', 'Heideck'],
    'B': ['Frost', 'Heideck', 'Knutson'],
    'C': ['Frost', 'Heideck', 'Knutson', 'Lai'],
    'D': ['Frost', 'Gonzalez', 'Heideck'],
    'E': ['Frost', 'Gonzalez', 'Heideck', 'Mays']
}

correct_option = None
for letter, names in options.items():
    if set(names) == set(forced):
        correct_option = letter
        break

if correct_option:
    print(f"\nCorrect option: {correct_option}")
    print(f"answer:{correct_option}")
else:
    print("\nNo option matches the forced set.")
    print("Forced set:", forced)
    print("Options:", options)