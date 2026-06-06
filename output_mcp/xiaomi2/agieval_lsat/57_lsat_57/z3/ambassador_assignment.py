from z3 import *

solver = Solver()

# Candidates: Jaramillo, Kayne, Landon, Novetzke, Ong
# Countries: 0=unassigned, 1=Venezuela, 2=Yemen, 3=Zambia
J, K, L, N, O = Ints('J K L N O')
candidates = [J, K, L, N, O]

# Each candidate assigned to 0-3
for c in candidates:
    solver.add(And(c >= 0, c <= 3))

# Exactly 3 candidates are assigned (non-zero), 2 are unassigned (zero)
solver.add(Sum([If(c != 0, 1, 0) for c in candidates]) == 3)

# Each country gets exactly one ambassador
for country in [1, 2, 3]:
    solver.add(Sum([If(c == country, 1, 0) for c in candidates]) == 1)

# No two assigned candidates go to the same country
for i in range(len(candidates)):
    for j in range(i+1, len(candidates)):
        # If both assigned, they must differ
        solver.add(Implies(And(candidates[i] != 0, candidates[j] != 0), candidates[i] != candidates[j]))

# Constraint 1: Exactly one of Kayne or Novetzke is assigned (XOR)
solver.add(Xor(K != 0, N != 0))

# Constraint 2: If Jaramillo is assigned, then Kayne is assigned
solver.add(Implies(J != 0, K != 0))

# Constraint 3: If Ong is assigned to Venezuela, Kayne is not assigned to Yemen
solver.add(Implies(O == 1, K != 2))

# Constraint 4: If Landon is assigned, it is to Zambia
solver.add(Implies(L != 0, L == 3))

# Additional premise: Kayne is assigned to Yemen
solver.add(K == 2)

# Define answer options
opt_a = (J == 1)   # Jaramillo assigned to Venezuela
opt_b = (L == 3)   # Landon assigned to Zambia
opt_c = (O == 3)   # Ong assigned to Zambia
opt_d = (J == 0)   # Jaramillo not assigned
opt_e = (O == 0)   # Ong not assigned

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")

# Also print a sample model for verification
solver.push()
if solver.check() == sat:
    m = solver.model()
    print("\nSample model:")
    for c, name in [(J, "Jaramillo"), (K, "Kayne"), (L, "Landon"), (N, "Novetzke"), (O, "Ong")]:
        val = m[c].as_long()
        country_map = {0: "unassigned", 1: "Venezuela", 2: "Yemen", 3: "Zambia"}
        print(f"  {name} -> {country_map[val]}")
solver.pop()