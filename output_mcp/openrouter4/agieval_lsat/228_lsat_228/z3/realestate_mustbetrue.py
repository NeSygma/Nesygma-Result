from z3 import *

# Buildings and their classes (weight: c1=4, c2=2, c3=1)
building_class = {
    "G": 1, "Y": 3, "Z": 3,  # RealProp initially
    "F": 1, "L": 2,          # Southco initially
    "K": 2, "M": 2, "O": 2   # Trustcorp initially
}

names = ["G", "Y", "Z", "F", "L", "K", "M", "O"]

# Owner variables: 0=RealProp, 1=Southco, 2=Trustcorp
owner = {b: Int(f"owner_{b}") for b in names}

# Base premises
premises = []

# Domain: each building owned by one of the 3 companies
for b in names:
    premises.append(owner[b] >= 0)
    premises.append(owner[b] <= 2)

# Total count of each class must be preserved
class1_total = Sum([If(building_class[b] == 1, 1, 0) for b in names])
class2_total = Sum([If(building_class[b] == 2, 1, 0) for b in names])
class3_total = Sum([If(building_class[b] == 3, 1, 0) for b in names])

premises.append(class1_total == 2)  # G, F
premises.append(class2_total == 4)  # L, K, M, O
premises.append(class3_total == 2)  # Y, Z

# Weight per company must be conserved (initial: each company has weight 6)
for company in range(3):
    w = Sum([If(owner[b] == company,
                If(building_class[b] == 1, 4,
                   If(building_class[b] == 2, 2, 1)),
                0) for b in names])
    premises.append(w == 6)

# RealProp owns only class 2 buildings
for b in names:
    if building_class[b] != 2:
        premises.append(owner[b] != 0)

# RealProp must own exactly 3 class 2 buildings (since weight=6, each c2=2)
realprop_c2_count = Sum([If(And(owner[b] == 0, building_class[b] == 2), 1, 0) for b in names])
premises.append(realprop_c2_count == 3)

# Now check each option using negation (entailment test)
# Option X "must be true" iff premises + Not(X) is unsat

found_options = []

# A: Trustcorp owns a class 1 building
opt_a = Or([And(owner[b] == 2, building_class[b] == 1) for b in names])

# B: Trustcorp owns the Meyer Building (M)
opt_b = (owner["M"] == 2)

# C: Southco owns a class 2 building
opt_c = Or([And(owner[b] == 1, building_class[b] == 2) for b in names])

# D: Southco owns both class 3 buildings (Y and Z)
opt_d = And(owner["Y"] == 1, owner["Z"] == 1)

# E: Southco owns the Flores Tower (F)
opt_e = (owner["F"] == 1)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    s = Solver()
    s.add(premises)
    s.add(Not(constr))  # Negate the option
    if s.check() == unsat:
        # premises + Not(option) is unsat => option must be true
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