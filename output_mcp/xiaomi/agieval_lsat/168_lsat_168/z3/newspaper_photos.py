from z3 import *

solver = Solver()

# Variables: number of photos by each photographer in each section
# Fuentes: F_L, F_M, F_S
# Gagnon: G_L, G_M, G_S
# Hue: H_L, H_M, H_S
F_L, F_M, F_S = Ints('F_L F_M F_S')
G_L, G_M, G_S = Ints('G_L G_M G_S')
H_L, H_M, H_S = Ints('H_L H_M H_S')

# Each section has exactly 2 photos
solver.add(F_L + G_L + H_L == 2)
solver.add(F_M + G_M + H_M == 2)
solver.add(F_S + G_S + H_S == 2)

# All counts are non-negative
for v in [F_L, F_M, F_S, G_L, G_M, G_S, H_L, H_M, H_S]:
    solver.add(v >= 0)

# For each photographer, at least 1 but no more than 3 of their photos must appear
solver.add(F_L + F_M + F_S >= 1, F_L + F_M + F_S <= 3)
solver.add(G_L + G_M + G_S >= 1, G_L + G_M + G_S <= 3)
solver.add(H_L + H_M + H_S >= 1, H_L + H_M + H_S <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one in Metro
# This means: there exists a photographer X such that X_L >= 1 and X_M >= 1
solver.add(Or(
    And(F_L >= 1, F_M >= 1),
    And(G_L >= 1, G_M >= 1),
    And(H_L >= 1, H_M >= 1)
))

# The number of Hue's photographs in Lifestyle must equal the number of Fuentes photographs in Sports
solver.add(H_L == F_S)

# None of Gagnon's photographs can be in the Sports section
solver.add(G_S == 0)

# Define option constraints
opt_a = And(
    F_L == 2, G_L == 0, H_L == 0,
    F_M == 1, G_M == 0, H_M == 1,
    F_S == 0, G_S == 1, H_S == 1
)

opt_b = And(
    F_L == 1, G_L == 1, H_L == 0,
    F_M == 1, G_M == 1, H_M == 0,
    F_S == 0, G_S == 0, H_S == 2
)

opt_c = And(
    F_L == 2, G_L == 0, H_L == 0,
    F_M == 0, G_M == 2, H_M == 0,
    F_S == 0, G_S == 0, H_S == 2
)

opt_d = And(
    F_L == 0, G_L == 2, H_L == 0,
    F_M == 1, G_M == 1, H_M == 0,
    F_S == 1, G_S == 0, H_S == 1
)

opt_e = And(
    F_L == 0, G_L == 1, H_L == 1,
    F_M == 0, G_M == 0, H_M == 2,
    F_S == 1, G_S == 0, H_S == 1
)

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