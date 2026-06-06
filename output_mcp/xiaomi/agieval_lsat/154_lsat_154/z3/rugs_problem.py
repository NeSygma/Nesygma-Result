from z3 import *

solver = Solver()

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
# 3 rugs: rug 0, 1, 2
# For each color, which rug is it assigned to? -1 means not used
N_COLORS = 6
N_RUGS = 3

# assignment[c] = rug index (0,1,2) if color c is used, or -1 if not used
assignment = [Int(f'assign_{c}') for c in range(N_COLORS)]

# Each color is either assigned to a rug (0,1,2) or not used (-1)
for c in range(N_COLORS):
    solver.add(Or(assignment[c] == -1, assignment[c] == 0, assignment[c] == 1, assignment[c] == 2))

# Exactly 5 of 6 colors are used (exactly one is -1)
solver.add(Sum([If(assignment[c] == -1, 1, 0) for c in range(N_COLORS)]) == 1)

# Count colors per rug
colors_in_rug = [Int(f'colors_in_rug_{r}') for r in range(N_RUGS)]
for r in range(N_RUGS):
    solver.add(colors_in_rug[r] == Sum([If(assignment[c] == r, 1, 0) for c in range(N_COLORS)]))
    solver.add(colors_in_rug[r] >= 1)

# GIVEN: One of the rugs is solid yellow
# Yellow (color 5) is used, and the rug it's in has exactly 1 color
solver.add(assignment[5] != -1)
# The rug containing yellow has exactly 1 color
for r in range(N_RUGS):
    solver.add(Implies(assignment[5] == r, colors_in_rug[r] == 1))

# RULE 1: In any rug with white, two other colors are also used (white rug has 3+ colors)
for r in range(N_RUGS):
    solver.add(Implies(assignment[4] == r, colors_in_rug[r] >= 3))

# RULE 2: In any rug with olive, peach is also used (same rug)
solver.add(Implies(assignment[1] != -1, And(assignment[2] != -1, assignment[1] == assignment[2])))

# RULE 3: Forest and turquoise not together
solver.add(Or(assignment[0] == -1, assignment[3] == -1, assignment[0] != assignment[3]))

# RULE 4: Peach and turquoise not together
solver.add(Or(assignment[2] == -1, assignment[3] == -1, assignment[2] != assignment[3]))

# RULE 5: Peach and yellow not together
solver.add(Or(assignment[2] == -1, assignment[2] != assignment[5]))

# Now evaluate each option
# Option A: There is exactly one solid color rug
# Yellow rug is solid. "Exactly one solid" means the other two rugs each have 2+ colors.
opt_a = And(
    And([Implies(And(assignment[5] != r), colors_in_rug[r] >= 2) for r in range(N_RUGS)])
)

# Option B: One of the rugs is solid forest
# Forest (color 0) is used and its rug has exactly 1 color
opt_b = And(assignment[0] != -1, 
            Or([And(assignment[0] == r, colors_in_rug[r] == 1) for r in range(N_RUGS)]))

# Option C: Turquoise is not used in any rug
opt_c = (assignment[3] == -1)

# Option D: Forest and olive are used together in a rug
opt_d = And(assignment[0] != -1, assignment[1] != -1, assignment[0] == assignment[1])

# Option E: Peach and white are used together in a rug
opt_e = And(assignment[2] != -1, assignment[4] != -1, assignment[2] == assignment[4])

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for c in range(N_COLORS):
            print(f"  Color {c} -> rug {m[assignment[c]]}")
        for r in range(N_RUGS):
            print(f"  Rug {r} has {m[colors_in_rug[r]]} colors")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print(f"\nFound options: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")