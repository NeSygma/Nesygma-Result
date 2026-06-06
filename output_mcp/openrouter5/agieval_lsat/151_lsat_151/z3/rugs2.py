from z3 import *

# Let's rethink the modeling. We have 3 rugs, 6 colors, exactly 5 used.
# Each used color appears in exactly one rug.
# One rug is solid peach.

colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
c_idx = {c: i for i, c in enumerate(colors)}

# Let's use a different approach: each color is assigned to a rug (0,1,2) or unused (3).
# rug_assignment[c] = r means color c is used in rug r (r in 0..2), or 3 means unused.
rug_assignment = [Int(f"rug_{c}") for c in range(6)]

solver = Solver()

# Domain: each color is assigned to rug 0, 1, 2, or unused (3)
for c in range(6):
    solver.add(rug_assignment[c] >= 0, rug_assignment[c] <= 3)

# Exactly 5 colors are used, so exactly one color is unused (assigned to 3)
solver.add(PbEq([(rug_assignment[c] == 3, 1) for c in range(6)], 1))

# Each used color appears in exactly one rug (already enforced by assignment being a single value)

# Rule: In any rug in which white is used, two other colors are also used.
# So if white is assigned to rug r (r != 3), then exactly 3 colors total are assigned to rug r.
for r in range(3):
    # Count colors assigned to rug r
    solver.add(Implies(rug_assignment[c_idx["white"]] == r,
                       PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 3)))

# Rule: In any rug in which olive is used, peach is also used.
for r in range(3):
    solver.add(Implies(rug_assignment[c_idx["olive"]] == r,
                       rug_assignment[c_idx["peach"]] == r))

# Rule: Forest and turquoise are not used together in a rug.
for r in range(3):
    solver.add(Not(And(rug_assignment[c_idx["forest"]] == r,
                       rug_assignment[c_idx["turquoise"]] == r)))

# Rule: Peach and turquoise are not used together in a rug.
for r in range(3):
    solver.add(Not(And(rug_assignment[c_idx["peach"]] == r,
                       rug_assignment[c_idx["turquoise"]] == r)))

# Rule: Peach and yellow are not used together in a rug.
for r in range(3):
    solver.add(Not(And(rug_assignment[c_idx["peach"]] == r,
                       rug_assignment[c_idx["yellow"]] == r)))

# Given: One of the rugs is solid peach.
# Solid peach means: peach is assigned to some rug r, and no other color is assigned to rug r.
# So rug r has exactly one color: peach.
solid_peach_rug = False
for r in range(3):
    # Count colors in rug r
    solver.add(Implies(rug_assignment[c_idx["peach"]] == r,
                       PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 1)))

# Now evaluate each option
# Option A: One of the rugs is solid forest.
opt_a = Or([And(rug_assignment[c_idx["forest"]] == r,
                PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 1)) for r in range(3)])

# Option B: One of the rugs is solid turquoise.
opt_b = Or([And(rug_assignment[c_idx["turquoise"]] == r,
                PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 1)) for r in range(3)])

# Option C: One of the rugs is solid yellow.
opt_c = Or([And(rug_assignment[c_idx["yellow"]] == r,
                PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 1)) for r in range(3)])

# Option D: Forest and white are used together in a rug.
opt_d = Or([And(rug_assignment[c_idx["forest"]] == r,
                rug_assignment[c_idx["white"]] == r) for r in range(3)])

# Option E: White and yellow are used together in a rug.
opt_e = Or([And(rug_assignment[c_idx["white"]] == r,
                rug_assignment[c_idx["yellow"]] == r) for r in range(3)])

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