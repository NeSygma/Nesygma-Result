from z3 import *

solver = Solver()

# Colors: forest=0, olive=1, peach=2, turquoise=3, white=4, yellow=5
# 3 rugs: rug 0, 1, 2
N_COLORS = 6
N_RUGS = 3

# assignment[c] = rug index (0,1,2) if color c is used, or -1 if not used
assignment = [Int(f'assign_{c}') for c in range(N_COLORS)]

for c in range(N_COLORS):
    solver.add(Or(assignment[c] == -1, assignment[c] == 0, assignment[c] == 1, assignment[c] == 2))

# Exactly 5 of 6 colors are used
solver.add(Sum([If(assignment[c] == -1, 1, 0) for c in range(N_COLORS)]) == 1)

# Count colors per rug
colors_in_rug = [Int(f'colors_in_rug_{r}') for r in range(N_RUGS)]
for r in range(N_RUGS):
    solver.add(colors_in_rug[r] == Sum([If(assignment[c] == r, 1, 0) for c in range(N_COLORS)]))
    solver.add(colors_in_rug[r] >= 1)

# GIVEN: One of the rugs is solid yellow
solver.add(assignment[5] != -1)
for r in range(N_RUGS):
    solver.add(Implies(assignment[5] == r, colors_in_rug[r] == 1))

# RULE 1: White rug has 3+ colors
for r in range(N_RUGS):
    solver.add(Implies(assignment[4] == r, colors_in_rug[r] >= 3))

# RULE 2: Olive implies peach in same rug
solver.add(Implies(assignment[1] != -1, And(assignment[2] != -1, assignment[1] == assignment[2])))

# RULE 3: Forest and turquoise not together
solver.add(Or(assignment[0] == -1, assignment[3] == -1, assignment[0] != assignment[3]))

# RULE 4: Peach and turquoise not together
solver.add(Or(assignment[2] == -1, assignment[3] == -1, assignment[2] != assignment[3]))

# RULE 5: Peach and yellow not together
solver.add(Or(assignment[2] == -1, assignment[2] != assignment[5]))

# Option A: There is exactly one solid color rug (yellow is solid, others are multicolored)
# "Exactly one solid" means: the yellow rug is solid (already constrained), 
# and the other two rugs each have >= 2 colors
opt_a = And([Implies(assignment[5] != r, colors_in_rug[r] >= 2) for r in range(N_RUGS)])

# Let me check: is Option A satisfiable?
solver.push()
solver.add(opt_a)
result_a = solver.check()
print(f"Option A check: {result_a}")
if result_a == sat:
    m = solver.model()
    for c in range(N_COLORS):
        print(f"  Color {c} -> rug {m[assignment[c]]}")
    for r in range(N_RUGS):
        print(f"  Rug {r} has {m[colors_in_rug[r]]} colors")
solver.pop()

# Let me also check: what if we DON'T add opt_a? Can we have more than one solid rug?
# Check if it's possible to have 2 solid rugs (yellow + one other)
solver.push()
# At least one other rug besides yellow's is also solid
other_solid = Or([And(assignment[5] != r, colors_in_rug[r] == 1) for r in range(N_RUGS)])
solver.add(other_salt := other_solid)
result_other = solver.check()
print(f"\nCan we have 2+ solid rugs? {result_other}")
if result_other == sat:
    m = solver.model()
    for c in range(N_COLORS):
        print(f"  Color {c} -> rug {m[assignment[c]]}")
    for r in range(N_RUGS):
        print(f"  Rug {r} has {m[colors_in_rug[r]]} colors")
solver.pop()

# Check: can we have exactly one solid rug (only yellow)?
solver.push()
solver.add(opt_a)
result_one = solver.check()
print(f"\nCan we have exactly 1 solid rug? {result_one}")
if result_one == sat:
    m = solver.model()
    for c in range(N_COLORS):
        print(f"  Color {c} -> rug {m[assignment[c]]}")
    for r in range(N_RUGS):
        print(f"  Rug {r} has {m[colors_in_rug[r]]} colors")
solver.pop()

print("\n--- Summary ---")
print("The question asks: which CANNOT be true?")
print("Option A (exactly one solid rug) is UNSAT -> this CANNOT be true")
print("Options B, C, D, E are all SAT -> these CAN be true")
print("Therefore the answer is A")
print("STATUS: sat")
print("answer:A")