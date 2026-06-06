from z3 import *

solver = Solver()

# Variables for Fuentes (F), Gagnon (G), Hue (H) in Lifestyle (L), Metro (M), Sports (S)
F_L, F_M, F_S = Int('F_L'), Int('F_M'), Int('F_S')
G_L, G_M, G_S = Int('G_L'), Int('G_M'), Int('G_S')
H_L, H_M, H_S = Int('H_L'), Int('H_M'), Int('H_S')

# Total photographs per photographer
F_total = F_L + F_M + F_S
G_total = G_L + G_M + G_S
H_total = H_L + H_M + H_S

# Total photographs per section
L_total = F_L + G_L + H_L
M_total = F_M + G_M + H_M
S_total = F_S + G_S + H_S

# Constraints
solver.add(L_total == 2)
solver.add(M_total == 2)
solver.add(S_total == 2)
solver.add(F_total >= 1, F_total <= 3)
solver.add(G_total >= 1, G_total <= 3)
solver.add(H_total >= 1, H_total <= 3)
solver.add(G_S == 0)  # Gagnon cannot be in Sports
solver.add(H_L == F_S)  # Hue's Lifestyle = Fuentes' Sports
solver.add(F_total + G_total + H_total == 6)

# At least one photographer in Lifestyle must also be in Metro
# This means at least one of F_L, G_L, or H_L must be > 0, and the same photographer must have at least one in Metro
solver.add(Or(And(F_L > 0, F_M > 0), And(G_L > 0, G_M > 0), And(H_L > 0, H_M > 0)))

# Additional constraint: The photographer who has a photograph in Lifestyle and Metro must be the same as the one who satisfies H_L == F_S
# This ensures that the constraint is more strictly applied
solver.add(Or(
    And(F_L > 0, F_M > 0, H_L == F_S, F_S > 0),  # Fuentes is the one with Lifestyle and Metro, and Hue's Lifestyle = Fuentes' Sports
    And(G_L > 0, G_M > 0, H_L == F_S, F_S == 0),  # Gagnon is the one with Lifestyle and Metro, and Hue's Lifestyle = Fuentes' Sports (Fuentes has 0 in Sports)
    And(H_L > 0, H_M > 0, H_L == F_S)  # Hue is the one with Lifestyle and Metro, and Hue's Lifestyle = Fuentes' Sports
))

# Answer choices for Fuentes' photographs
# (A) One in Lifestyle, one in Metro, one in Sports
opt_a = And(F_L == 1, F_M == 1, F_S == 1)
# (B) One in Lifestyle, two in Sports
opt_b = And(F_L == 1, F_M == 0, F_S == 2)
# (C) Two in Lifestyle, one in Sports
opt_c = And(F_L == 2, F_M == 0, F_S == 1)
# (D) One in Metro, two in Sports
opt_d = And(F_L == 0, F_M == 1, F_S == 2)
# (E) Two in Metro, one in Sports
opt_e = And(F_L == 0, F_M == 2, F_S == 1)

# Evaluate each option
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