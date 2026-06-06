from z3 import *

# Countries
Venezuela, Yemen, Zambia = 0, 1, 2
countries = ["Venezuela", "Yemen", "Zambia"]

# Candidates
Jaramillo, Kayne, Landon, Novetzke, Ong = 0, 1, 2, 3, 4
candidates = ["Jaramillo", "Kayne", "Landon", "Novetzke", "Ong"]

# We'll use Int variables: assign[country] = candidate index
assign = [Int(f"assign_{c}") for c in range(3)]  # 0=Venezuela, 1=Yemen, 2=Zambia

solver = Solver()

# Domain: each assignment is a candidate
for c in range(3):
    solver.add(assign[c] >= 0, assign[c] <= 4)

# Distinctness: no ambassador to more than one country
solver.add(Distinct(assign))

# Constraint 1: Exactly one of Kayne(1) or Novetzke(3) is assigned
# Count how many of {Kayne, Novetzke} are assigned (sum of presence)
solver.add(
    Sum([If(assign[c] == Kayne, 1, 0) for c in range(3)]) +
    Sum([If(assign[c] == Novetzke, 1, 0) for c in range(3)]) == 1
)

# Constraint 2: If Jaramillo(0) is assigned, then Kayne(1) is assigned
# Jaramillo assigned means sum of Jaramillo == 1
solver.add(
    Implies(
        Sum([If(assign[c] == Jaramillo, 1, 0) for c in range(3)]) == 1,
        Sum([If(assign[c] == Kayne, 1, 0) for c in range(3)]) == 1
    )
)

# Constraint 3: If Ong(4) is assigned to Venezuela(0), Kayne(1) is not assigned to Yemen(1)
solver.add(
    Implies(
        assign[Venezuela] == Ong,
        assign[Yemen] != Kayne
    )
)

# Constraint 4: If Landon(2) is assigned to an ambassadorship, it is to Zambia(2)
# Landon assigned => Landon is at Zambia
solver.add(
    Implies(
        Sum([If(assign[c] == Landon, 1, 0) for c in range(3)]) == 1,
        assign[Zambia] == Landon
    )
)

# Now evaluate each option
# Option A: Venezuela: Jaramillo (0), Yemen: Ong (4), Zambia: Novetzke (3)
opt_a = And(assign[Venezuela] == Jaramillo, assign[Yemen] == Ong, assign[Zambia] == Novetzke)

# Option B: Venezuela: Kayne (1), Yemen: Jaramillo (0), Zambia: Landon (2)
opt_b = And(assign[Venezuela] == Kayne, assign[Yemen] == Jaramillo, assign[Zambia] == Landon)

# Option C: Venezuela: Landon (2), Yemen: Novetzke (3), Zambia: Ong (4)
opt_c = And(assign[Venezuela] == Landon, assign[Yemen] == Novetzke, assign[Zambia] == Ong)

# Option D: Venezuela: Novetzke (3), Yemen: Jaramillo (0), Zambia: Kayne (1)
opt_d = And(assign[Venezuela] == Novetzke, assign[Yemen] == Jaramillo, assign[Zambia] == Kayne)

# Option E: Venezuela: Ong (4), Yemen: Kayne (1), Zambia: Landon (2)
opt_e = And(assign[Venezuela] == Ong, assign[Yemen] == Kayne, assign[Zambia] == Landon)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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