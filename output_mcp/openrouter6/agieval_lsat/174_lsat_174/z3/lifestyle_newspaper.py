from z3 import *

solver = Solver()

# Declare variables
L_f, L_g, L_h = Ints('L_f L_g L_h')
M_f, M_g, M_h = Ints('M_f M_g M_h')
S_f, S_g, S_h = Ints('S_f S_g S_h')

# Non-negativity
solver.add(L_f >= 0, L_g >= 0, L_h >= 0)
solver.add(M_f >= 0, M_g >= 0, M_h >= 0)
solver.add(S_f >= 0, S_g >= 0, S_h >= 0)

# Section totals (2 per section)
solver.add(L_f + L_g + L_h == 2)
solver.add(M_f + M_g + M_h == 2)
solver.add(S_f + S_g + S_h == 2)

# Photographer totals between 1 and 3
fuentes_total = L_f + M_f + S_f
gagnon_total = L_g + M_g + S_g
hue_total = L_h + M_h + S_h
solver.add(fuentes_total >= 1, fuentes_total <= 3)
solver.add(gagnon_total >= 1, gagnon_total <= 3)
solver.add(hue_total >= 1, hue_total <= 3)

# At least one photograph in Lifestyle must be by a photographer who has at least one in Metro
solver.add(Or(
    And(L_f > 0, M_f > 0),
    And(L_g > 0, M_g > 0),
    And(L_h > 0, M_h > 0)
))

# Number of Hue's photographs in Lifestyle equals number of Fuentes's photographs in Sports
solver.add(L_h == S_f)

# None of Gagnon's photographs can be in Sports
solver.add(S_g == 0)

# Given: one photograph in Metro is by Fuentes and one is by Hue
solver.add(M_f == 1)
solver.add(M_h == 1)
solver.add(M_g == 0)

# Now evaluate each answer choice
found_options = []

# Option A: Both photographs in Lifestyle are by Fuentes
opt_a = And(L_f == 2, L_g == 0, L_h == 0)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: Both photographs in Lifestyle are by Gagnon
opt_b = And(L_g == 2, L_f == 0, L_h == 0)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: One photograph in Lifestyle is by Gagnon and one is by Hue
opt_c = And(L_g == 1, L_h == 1, L_f == 0)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: Both photographs in Lifestyle are by Hue
opt_d = And(L_h == 2, L_f == 0, L_g == 0)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: Both photographs in Sports are by Fuentes
opt_e = And(S_f == 2, S_g == 0, S_h == 0)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output result
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")