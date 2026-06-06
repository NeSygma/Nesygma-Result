from z3 import *

solver = Solver()

# Variables for counts
L_F = Int('L_F')
L_G = Int('L_G')
L_H = Int('L_H')
M_F = Int('M_F')
M_G = Int('M_G')
M_H = Int('M_H')
S_F = Int('S_F')
S_G = Int('S_G')
S_H = Int('S_H')

# Each count between 0 and 2
solver.add(0 <= L_F, L_F <= 2)
solver.add(0 <= L_G, L_G <= 2)
solver.add(0 <= L_H, L_H <= 2)
solver.add(0 <= M_F, M_F <= 2)
solver.add(0 <= M_G, M_G <= 2)
solver.add(0 <= M_H, M_H <= 2)
solver.add(0 <= S_F, S_F <= 2)
solver.add(0 <= S_G, S_G <= 2)
solver.add(0 <= S_H, S_H <= 2)

# Each section has exactly two photos
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# Constraint 4: No Gagnon in Sports
solver.add(S_G == 0)

# Constraint 1: Each photographer appears between 1 and 3 times total
total_F = L_F + M_F + S_F
total_G = L_G + M_G + S_G
total_H = L_H + M_H + S_H
solver.add(total_F >= 1, total_F <= 3)
solver.add(total_G >= 1, total_G <= 3)
solver.add(total_H >= 1, total_H <= 3)

# Constraint 2: At least one photo in Lifestyle by a photographer who also has at least one in Metro
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Constraint 3: Number of Hue's photos in Lifestyle equals number of Fuentes photos in Sports
solver.add(L_H == S_F)

# Now evaluate each option
found_options = []

# Option A: L_F=1, M_F=1, S_F=1
opt_a = And(L_F == 1, M_F == 1, S_F == 1)
solver.push()
solver.add(opt_a)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: L_F=1, S_F=2, M_F=0
opt_b = And(L_F == 1, S_F == 2, M_F == 0)
solver.push()
solver.add(opt_b)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: L_F=2, S_F=1, M_F=0
opt_c = And(L_F == 2, S_F == 1, M_F == 0)
solver.push()
solver.add(opt_c)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: M_F=1, S_F=2, L_F=0
opt_d = And(M_F == 1, S_F == 2, L_F == 0)
solver.push()
solver.add(opt_d)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: M_F=2, S_F=1, L_F=0
opt_e = And(M_F == 2, S_F == 1, L_F == 0)
solver.push()
solver.add(opt_e)
if solver.check() == sat:
    found_options.append('E')
solver.pop()

# Output results
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")