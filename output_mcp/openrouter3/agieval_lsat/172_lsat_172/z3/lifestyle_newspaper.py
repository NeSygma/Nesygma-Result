from z3 import *

# Problem analysis:
# - 3 sections: Lifestyle (L), Metro (M), Sports (S)
# - 2 photos per section = 6 total photos
# - 3 photographers: Fuentes (F), Gagnon (G), Hue (H)
# - Each photographer: at least 1, at most 3 photos total
# - At least one L photo by photographer who also has at least one M photo
# - #H in L = #F in S
# - No G photos in S
# - Additional condition: one L photo by F, one L photo by H

# Create variables: For each section, we need to assign photographers to the 2 photos
# We'll use arrays: L[0], L[1] for Lifestyle photos; M[0], M[1] for Metro; S[0], S[1] for Sports
# Each variable can be F, G, or H (we'll use integers 0,1,2 for F,G,H)

F, G, H = 0, 1, 2  # photographers

# Decision variables
L = [Int(f'L_{i}') for i in range(2)]
M = [Int(f'M_{i}') for i in range(2)]
S = [Int(f'S_{i}') for i in range(2)]

solver = Solver()

# Domain constraints: each photo must be by one of the three photographers
for i in range(2):
    solver.add(Or(L[i] == F, L[i] == G, L[i] == H))
    solver.add(Or(M[i] == F, M[i] == G, M[i] == H))
    solver.add(Or(S[i] == F, S[i] == G, S[i] == H))

# Additional condition: one L photo by F, one L photo by H
# This means exactly one F and exactly one H in L (since there are 2 photos)
solver.add(Or(L[0] == F, L[1] == F))  # at least one F
solver.add(Or(L[0] == H, L[1] == H))  # at least one H
# And they must be different (since exactly one each)
solver.add(Or(And(L[0] == F, L[1] == H), And(L[0] == H, L[1] == F)))

# Count photos per photographer
# We'll count using If expressions
count_F = Sum([If(L[i] == F, 1, 0) for i in range(2)] +
              [If(M[i] == F, 1, 0) for i in range(2)] +
              [If(S[i] == F, 1, 0) for i in range(2)])
count_G = Sum([If(L[i] == G, 1, 0) for i in range(2)] +
              [If(M[i] == G, 1, 0) for i in range(2)] +
              [If(S[i] == G, 1, 0) for i in range(2)])
count_H = Sum([If(L[i] == H, 1, 0) for i in range(2)] +
              [If(M[i] == H, 1, 0) for i in range(2)] +
              [If(S[i] == H, 1, 0) for i in range(2)])

# Each photographer: at least 1, at most 3 photos
solver.add(count_F >= 1, count_F <= 3)
solver.add(count_G >= 1, count_G <= 3)
solver.add(count_H >= 1, count_H <= 3)

# At least one L photo by photographer who has at least one M photo
# This means: there exists a photographer P such that P has at least one L photo AND at least one M photo
# We'll encode this by checking each photographer
solver.add(Or(
    # Fuentes has at least one L and at least one M
    And(Or(L[0] == F, L[1] == F), Or(M[0] == F, M[1] == F)),
    # Gagnon has at least one L and at least one M
    And(Or(L[0] == G, L[1] == G), Or(M[0] == G, M[1] == G)),
    # Hue has at least one L and at least one M
    And(Or(L[0] == H, L[1] == H), Or(M[0] == H, M[1] == H))
))

# #H in L = #F in S
count_H_L = Sum([If(L[i] == H, 1, 0) for i in range(2)])
count_F_S = Sum([If(S[i] == F, 1, 0) for i in range(2)])
solver.add(count_H_L == count_F_S)

# No G photos in S
for i in range(2):
    solver.add(S[i] != G)

# Now evaluate each answer choice
found_options = []

# Option A: Both photographs in the Metro section are by Fuentes
opt_a = And(M[0] == F, M[1] == F)

# Option B: Both photographs in the Metro section are by Gagnon
opt_b = And(M[0] == G, M[1] == G)

# Option C: Exactly one photograph in the Metro section is by Hue
opt_c = Or(And(M[0] == H, M[1] != H), And(M[0] != H, M[1] == H))

# Option D: Both photographs in the Sports section are by Hue
opt_d = And(S[0] == H, S[1] == H)

# Option E: Neither photograph in the Sports section is by Hue
opt_e = And(S[0] != H, S[1] != H)

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