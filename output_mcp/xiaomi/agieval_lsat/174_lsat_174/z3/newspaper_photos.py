from z3 import *

solver = Solver()

# Sections: Lifestyle (L), Metro (M), Sports (S) - each has 2 photographs
# Photographers: Fuentes (F), Gagnon (G), Hue (H)
# Variables: photographer for each photo slot in each section
# L[0], L[1] = Lifestyle photos
# M[0], M[1] = Metro photos
# S[0], S[1] = Sports photos

# Each variable is 0=Fuentes, 1=Gagnon, 2=Hue
L = [Int(f'L_{i}') for i in range(2)]
M = [Int(f'M_{i}') for i in range(2)]
S = [Int(f'S_{i}') for i in range(2)]

# Domain constraints: each photo is by one of the three photographers
for v in L + M + S:
    solver.add(Or(v == 0, v == 1, v == 2))

# Count photos by each photographer
total_F = Sum([If(v == 0, 1, 0) for v in L + M + S])
total_G = Sum([If(v == 1, 1, 0) for v in L + M + S])
total_H = Sum([If(v == 2, 1, 0) for v in L + M + S])

# Condition 1: For each photographer, at least 1 but no more than 3
solver.add(total_F >= 1, total_F <= 3)
solver.add(total_G >= 1, total_G <= 3)
solver.add(total_H >= 1, total_H <= 3)

# Condition 2: At least one photograph in Lifestyle must be by a photographer
# who has at least one photograph in Metro section.
# For each Lifestyle photo, check if that photographer also has a Metro photo
for i in range(2):
    # L[i] == F and F has a Metro photo, OR L[i] == G and G has a Metro photo, OR L[i] == H and H has a Metro photo
    f_in_m = Or([M[j] == 0 for j in range(2)])
    g_in_m = Or([M[j] == 1 for j in range(2)])
    h_in_m = Or([M[j] == 2 for j in range(2)])
    solver.add(Implies(L[i] == 0, f_in_m))
    solver.add(Implies(L[i] == 1, g_in_m))
    solver.add(Implies(L[i] == 2, h_in_m))

# Condition 3: Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
hue_in_L = Sum([If(L[i] == 2, 1, 0) for i in range(2)])
fuentes_in_S = Sum([If(S[i] == 0, 1, 0) for i in range(2)])
solver.add(hue_in_L == fuentes_in_S)

# Condition 4: None of Gagnon's photographs can be in Sports
for i in range(2):
    solver.add(S[i] != 1)

# Additional given: One Metro photo is by Fuentes, one is by Hue
solver.add(Or(And(M[0] == 0, M[1] == 2), And(M[0] == 2, M[1] == 0)))

# Now test each answer option
found_options = []

# Option A: Both photographs in Lifestyle are by Fuentes
opt_a = And(L[0] == 0, L[1] == 0)

# Option B: Both photographs in Lifestyle are by Gagnon
opt_b = And(L[0] == 1, L[1] == 1)

# Option C: One Lifestyle photo by Gagnon, one by Hue
opt_c = Or(And(L[0] == 1, L[1] == 2), And(L[0] == 2, L[1] == 1))

# Option D: Both photographs in Lifestyle are by Hue
opt_d = And(L[0] == 2, L[1] == 2)

# Option E: Both photographs in Sports are by Fuentes
opt_e = And(S[0] == 0, S[1] == 0)

for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        print(f"  L = [{m[L[0]]}, {m[L[1]]}]")
        print(f"  M = [{m[M[0]]}, {m[M[1]]}]")
        print(f"  S = [{m[S[0]]}, {m[S[1]]}]")
    else:
        print(f"Option {letter} is UNSAT")
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