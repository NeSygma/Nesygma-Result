from z3 import *

solver = Solver()

# Variables: counts for each photographer in each section
# All counts are integers between 0 and 2
F_L, F_M, F_S = Ints('F_L F_M F_S')
G_L, G_M, G_S = Ints('G_L G_M G_S')
H_L, H_M, H_S = Ints('H_L H_M H_S')

# Domain constraints: each count is 0, 1, or 2
for var in [F_L, F_M, F_S, G_L, G_M, G_S, H_L, H_M, H_S]:
    solver.add(And(var >= 0, var <= 2))

# Total photos per section = 2
solver.add(F_L + G_L + H_L == 2)
solver.add(F_M + G_M + H_M == 2)
solver.add(F_S + G_S + H_S == 2)

# Each photographer has between 1 and 3 total photos
solver.add(Sum([F_L, F_M, F_S]) >= 1, Sum([F_L, F_M, F_S]) <= 3)
solver.add(Sum([G_L, G_M, G_S]) >= 1, Sum([G_L, G_M, G_S]) <= 3)
solver.add(Sum([H_L, H_M, H_S]) >= 1, Sum([H_L, H_M, H_S]) <= 3)

# Constraint 2: At least one Lifestyle photo by a photographer who also has a Metro photo
solver.add(Or(
    And(F_L >= 1, F_M >= 1),
    And(G_L >= 1, G_M >= 1),
    And(H_L >= 1, H_M >= 1)
))

# Constraint 3: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
solver.add(H_L == F_S)

# Constraint 4: No Gagnon photos in Sports
solver.add(G_S == 0)

# Given: One Lifestyle photo by Fuentes and one by Hue
solver.add(F_L == 1)
solver.add(H_L == 1)
# Since F_L + G_L + H_L = 2, we get G_L = 0
# But let's add it explicitly for safety
solver.add(G_L == 0)

# Now check each option
found_options = []

# Option A: Both Metro photos by Fuentes
opt_a = And(F_M == 2, G_M == 0, H_M == 0)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append("A")
solver.pop()

# Option B: Both Metro photos by Gagnon
opt_b = And(G_M == 2, F_M == 0, H_M == 0)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append("B")
solver.pop()

# Option C: Exactly one Metro photo by Hue
opt_c = And(H_M == 1)
# The rest could be any valid distribution
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append("C")
solver.pop()

# Option D: Both Sports photos by Hue
opt_d = And(H_S == 2, F_S == 0, G_S == 0)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append("D")
solver.pop()

# Option E: Neither Sports photo by Hue
opt_e = And(H_S == 0)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append("E")
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