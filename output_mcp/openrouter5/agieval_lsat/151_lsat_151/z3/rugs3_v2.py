from z3 import *

# Let's rethink the modeling.
# We have 3 rugs, 6 colors, exactly 5 used.
# Each used color appears in exactly one rug.
# One rug is solid peach.

colors = ["forest", "olive", "peach", "turquoise", "white", "yellow"]
c_idx = {c: i for i, c in enumerate(colors)}

# rug_assignment[c] = r means color c is used in rug r (r in 0..2), or 3 means unused.
rug_assignment = [Int(f"rug_{c}") for c in range(6)]

solver = Solver()

# Domain
for c in range(6):
    solver.add(rug_assignment[c] >= 0, rug_assignment[c] <= 3)

# Exactly 5 colors are used, so exactly one color is unused (assigned to 3)
solver.add(PbEq([(rug_assignment[c] == 3, 1) for c in range(6)], 1))

# Rule: In any rug in which white is used, two other colors are also used.
# So if white is assigned to rug r (r != 3), then exactly 3 colors total are assigned to rug r.
for r in range(3):
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
solver.add(Or([And(rug_assignment[c_idx["peach"]] == r,
                   PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 1)) for r in range(3)]))

# Let's enumerate all solutions to see what MUST be true
# First, let's check if the base constraints are satisfiable
print("Checking base constraints...")
result = solver.check()
print(f"Base result: {result}")

# Enumerate all solutions
solutions = []
while solver.check() == sat:
    m = solver.model()
    sol = tuple(m.eval(rug_assignment[c]) for c in range(6))
    solutions.append(sol)
    # Block this solution
    solver.add(Or([rug_assignment[c] != m.eval(rug_assignment[c]) for c in range(6)]))

print(f"Total solutions: {len(solutions)}")
for sol in solutions:
    print(f"  {[colors[i] + ':' + str(sol[i]) for i in range(6)]}")

# Now let's check each option across all solutions
# We need to find which option is true in ALL solutions (must be true)

# Re-create solver for checking each option
def check_option(constr):
    s = Solver()
    # Add all base constraints
    for c in range(6):
        s.add(rug_assignment[c] >= 0, rug_assignment[c] <= 3)
    s.add(PbEq([(rug_assignment[c] == 3, 1) for c in range(6)], 1))
    for r in range(3):
        s.add(Implies(rug_assignment[c_idx["white"]] == r,
                       PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 3)))
    for r in range(3):
        s.add(Implies(rug_assignment[c_idx["olive"]] == r,
                       rug_assignment[c_idx["peach"]] == r))
    for r in range(3):
        s.add(Not(And(rug_assignment[c_idx["forest"]] == r,
                       rug_assignment[c_idx["turquoise"]] == r)))
    for r in range(3):
        s.add(Not(And(rug_assignment[c_idx["peach"]] == r,
                       rug_assignment[c_idx["turquoise"]] == r)))
    for r in range(3):
        s.add(Not(And(rug_assignment[c_idx["peach"]] == r,
                       rug_assignment[c_idx["yellow"]] == r)))
    s.add(Or([And(rug_assignment[c_idx["peach"]] == r,
                   PbEq([(rug_assignment[c] == r, 1) for c in range(6)], 1)) for r in range(3)]))
    # Add the negation of the option - if it's unsatisfiable, the option MUST be true
    s.add(Not(constr))
    return s.check()

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

print("\nChecking which options MUST be true (negation is unsat):")
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    res = check_option(constr)
    print(f"  Option {letter}: negation is {res}")