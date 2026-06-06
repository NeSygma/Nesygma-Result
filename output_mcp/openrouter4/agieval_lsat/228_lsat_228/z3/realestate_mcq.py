from z3 import *

# Buildings and their classes
building_class = {
    "G": 1, "Y": 3, "Z": 3, "F": 1, "L": 2, "K": 2, "M": 2, "O": 2
}

buildings = ["G", "Y", "Z", "F", "L", "K", "M", "O"]

# Owner variables: 0=RealProp, 1=Southco, 2=Trustcorp
owner = {b: Int(f"owner_{b}") for b in buildings}

# Base solver with constraints
solver = Solver()

for b in buildings:
    solver.add(owner[b] >= 0, owner[b] <= 2)

# RealProp must own only class 2 buildings
for b in buildings:
    if building_class[b] != 2:
        solver.add(owner[b] != 0)

# RealProp must own at least 1 class 2 building (to own "only class 2 buildings")
realprop_class2_count = Sum([If(And(owner[b] == 0, building_class[b] == 2), 1, 0) for b in buildings])
solver.add(realprop_class2_count >= 1)

# Weighted sum invariant: each company's (4*c1 + 2*c2 + 1*c3) is preserved
# Initial: RealProp: 4*1 + 2*0 + 1*2 = 6, Southco: 4*1 + 2*1 + 1*0 = 6, Trustcorp: 4*0 + 2*3 + 1*0 = 6
# Since RealProp ends with only class 2, weight*2 = 2*k = 6, so k=3
solver.add(realprop_class2_count == 3)

# Southco and Trustcorp weighted sums
southco_w = Sum([If(owner[b] == 1,
                    If(building_class[b] == 1, 4,
                       If(building_class[b] == 2, 2, 1)),
                    0) for b in buildings])

trustcorp_w = Sum([If(owner[b] == 2,
                      If(building_class[b] == 1, 4,
                         If(building_class[b] == 2, 2, 1)),
                      0) for b in buildings])

solver.add(southco_w == 6)
solver.add(trustcorp_w == 6)

# Now evaluate each option
found_options = []

# A: Trustcorp owns a class 1 building
opt_a = Or([And(owner[b] == 2, building_class[b] == 1) for b in buildings])

# B: Trustcorp owns the Meyer Building
opt_b = (owner["M"] == 2)

# C: Southco owns a class 2 building
opt_c = Or([And(owner[b] == 1, building_class[b] == 2) for b in buildings])

# D: Southco owns both class 3 buildings
opt_d = And(owner["Y"] == 1, owner["Z"] == 1)

# E: Southco owns the Flores Tower
opt_e = (owner["F"] == 1)

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