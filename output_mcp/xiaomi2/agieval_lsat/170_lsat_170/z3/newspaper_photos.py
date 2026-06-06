from z3 import *

solver = Solver()

# Sections: Lifestyle (L), Metro (M), Sports (S)
# Photographers: Fuentes (F), Gagnon (G), Hue (H)
# Variables: count of each photographer's photos in each section
L_F, L_G, L_H = Ints('L_F L_G L_H')
M_F, M_G, M_H = Ints('M_F M_G M_H')
S_F, S_G, S_H = Ints('S_F S_G S_H')

# Each section has exactly 2 photographs
solver.add(L_F + L_G + L_H == 2)
solver.add(M_F + M_G + M_H == 2)
solver.add(S_F + S_G + S_H == 2)

# All counts are non-negative
for v in [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]:
    solver.add(v >= 0)

# Constraint 1: Each photographer has at least 1 and at most 3 total
solver.add(L_F + M_F + S_F >= 1, L_F + M_F + S_F <= 3)
solver.add(L_G + M_G + S_G >= 1, L_G + M_G + S_G <= 3)
solver.add(L_H + M_H + S_H >= 1, L_H + M_H + S_H <= 3)

# Constraint 2: At least one Lifestyle photo is by a photographer with >=1 Metro photo
solver.add(Or(
    And(L_F >= 1, M_F >= 1),
    And(L_G >= 1, M_G >= 1),
    And(L_H >= 1, M_H >= 1)
))

# Constraint 3: Number of Hue's photos in Lifestyle = Number of Fuentes' photos in Sports
solver.add(L_H == S_F)

# Constraint 4: None of Gagnon's photos in Sports
solver.add(S_G == 0)

# Additional condition: One Lifestyle photo by Gagnon, one by Hue
solver.add(L_G == 1)
solver.add(L_H == 1)
# Therefore L_F = 0
solver.add(L_F == 0)

# Define answer choice constraints
# (A) Exactly one Metro photo by Fuentes
opt_a = (M_F == 1)
# (B) Exactly one Metro photo by Gagnon
opt_b = (M_G == 1)
# (C) Both Metro photos by Gagnon
opt_c = (M_G == 2)
# (D) Exactly one Sports photo by Hue
opt_d = (S_H == 1)
# (E) Both Sports photos by Hue
opt_e = (S_H == 2)

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

# Also print all valid configurations for verification
print("\n--- All valid Metro/Sports configurations ---")
s2 = Solver()
# Copy all base constraints
s2.add(L_F + L_G + L_H == 2)
s2.add(M_F + M_G + M_H == 2)
s2.add(S_F + S_G + S_H == 2)
for v in [L_F, L_G, L_H, M_F, M_G, M_H, S_F, S_G, S_H]:
    s2.add(v >= 0)
s2.add(L_F + M_F + S_F >= 1, L_F + M_F + S_F <= 3)
s2.add(L_G + M_G + S_G >= 1, L_G + M_G + S_G <= 3)
s2.add(L_H + M_H + S_H >= 1, L_H + M_H + S_H <= 3)
s2.add(Or(And(L_F >= 1, M_F >= 1), And(L_G >= 1, M_G >= 1), And(L_H >= 1, M_H >= 1)))
s2.add(L_H == S_F)
s2.add(S_G == 0)
s2.add(L_G == 1, L_H == 1, L_F == 0)

count = 0
while s2.check() == sat:
    m = s2.model()
    count += 1
    print(f"Config {count}: Metro=(F={m[M_F]},G={m[M_G]},H={m[M_H]}), Sports=(F={m[S_F]},G={m[S_G]},H={m[S_H]})")
    s2.add(Or(M_F != m[M_F], M_G != m[M_G], M_H != m[M_H], S_F != m[S_F], S_H != m[S_H]))
print(f"Total configurations: {count}")