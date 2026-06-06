from z3 import *

solver = Solver()

# Sections: Lifestyle (L), Metro (M), Sports (S)
# Photographers: Fuentes (F), Gagnon (G), Hue (H)

# Variables: number of photos by each photographer in each section
# F_L, F_M, F_S = Fuentes photos in Lifestyle, Metro, Sports
# G_L, G_M, G_S = Gagnon photos in Lifestyle, Metro, Sports
# H_L, H_M, H_S = Hue photos in Lifestyle, Metro, Sports

F_L = Int('F_L')
F_M = Int('F_M')
F_S = Int('F_S')
G_L = Int('G_L')
G_M = Int('G_M')
G_S = Int('G_S')
H_L = Int('H_L')
H_M = Int('H_M')
H_S = Int('H_S')

# All counts are non-negative
for v in [F_L, F_M, F_S, G_L, G_M, G_S, H_L, H_M, H_S]:
    solver.add(v >= 0)

# Exactly two photographs per section
solver.add(F_L + G_L + H_L == 2)
solver.add(F_M + G_M + H_M == 2)
solver.add(F_S + G_S + H_S == 2)

# Total of six different photographs
# (already implied by 2+2+2=6)

# For each photographer, at least one but no more than three of that photographer's photographs must appear
solver.add(F_L + F_M + F_S >= 1)
solver.add(F_L + F_M + F_S <= 3)
solver.add(G_L + G_M + G_S >= 1)
solver.add(G_L + G_M + G_S <= 3)
solver.add(H_L + H_M + H_S >= 1)
solver.add(H_L + H_M + H_S <= 3)

# At least one photograph in the Lifestyle section must be by a photographer who has at least one photograph in the Metro section.
# This means: there exists a photographer P such that P has >=1 in Lifestyle AND P has >=1 in Metro
# We need: (F_L >= 1 AND F_M >= 1) OR (G_L >= 1 AND G_M >= 1) OR (H_L >= 1 AND H_M >= 1)
solver.add(Or(
    And(F_L >= 1, F_M >= 1),
    And(G_L >= 1, G_M >= 1),
    And(H_L >= 1, H_M >= 1)
))

# The number of Hue's photographs in the Lifestyle section must be the same as the number of Fuentes photographs in the Sports section
solver.add(H_L == F_S)

# None of Gagnon's photographs can be in the Sports section
solver.add(G_S == 0)

# Now evaluate each answer choice for Fuentes
# (A) One is in the Lifestyle section, one is in the Metro section, and one is in the Sports section.
opt_a = And(F_L == 1, F_M == 1, F_S == 1)

# (B) One is in the Lifestyle section, and two are in the Sports section.
opt_b = And(F_L == 1, F_S == 2)

# (C) Two are in the Lifestyle section, and one is in the Sports section.
opt_c = And(F_L == 2, F_S == 1)

# (D) One is in the Metro section, and two are in the Sports section.
opt_d = And(F_M == 1, F_S == 2)

# (E) Two are in the Metro section, and one is in the Sports section.
opt_e = And(F_M == 2, F_S == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        print(f"  F_L={m[F_L]}, F_M={m[F_M]}, F_S={m[F_S]}")
        print(f"  G_L={m[G_L]}, G_M={m[G_M]}, G_S={m[G_S]}")
        print(f"  H_L={m[H_L]}, H_M={m[H_M]}, H_S={m[H_S]}")
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