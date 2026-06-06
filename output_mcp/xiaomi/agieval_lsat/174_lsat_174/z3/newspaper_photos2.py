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
# This means: there exists some photographer P such that P has >=1 photo in Lifestyle AND >=1 photo in Metro
# Let's express this as: at least one Lifestyle photo's photographer also appears in Metro
solver.add(Or(
    And(L[0] == 0, Or(M[0] == 0, M[1] == 0)),  # L[0] is Fuentes and Fuentes in Metro
    And(L[0] == 1, Or(M[0] == 1, M[1] == 1)),  # L[0] is Gagnon and Gagnon in Metro
    And(L[0] == 2, Or(M[0] == 2, M[1] == 2)),  # L[0] is Hue and Hue in Metro
    And(L[1] == 0, Or(M[0] == 0, M[1] == 0)),  # L[1] is Fuentes and Fuentes in Metro
    And(L[1] == 1, Or(M[0] == 1, M[1] == 1)),  # L[1] is Gagnon and Gagnon in Metro
    And(L[1] == 2, Or(M[0] == 2, M[1] == 2)),  # L[1] is Hue and Hue in Metro
))

# Condition 3: Number of Hue's photos in Lifestyle == Number of Fuentes photos in Sports
hue_in_L = Sum([If(L[i] == 2, 1, 0) for i in range(2)])
fuentes_in_S = Sum([If(S[i] == 0, 1, 0) for i in range(2)])
solver.add(hue_in_L == fuentes_in_S)

# Condition 4: None of Gagnon's photographs can be in Sports
for i in range(2):
    solver.add(S[i] != 1)

# Additional given: One Metro photo is by Fuentes, one is by Hue
solver.add(Or(And(M[0] == 0, M[1] == 2), And(M[0] == 2, M[1] == 0)))

# First, let's see if the base constraints are satisfiable
print("Checking base constraints...")
if solver.check() == sat:
    m = solver.model()
    print("Base constraints SAT:")
    print(f"  L = [{m[L[0]]}, {m[L[1]]}]")
    print(f"  M = [{m[M[0]]}, {m[M[1]]}]")
    print(f"  S = [{m[S[0]]}, {m[S[1]]}]")
    print(f"  total_F = {m.eval(total_F)}")
    print(f"  total_G = {m.eval(total_G)}")
    print(f"  total_H = {m.eval(total_H)}")
else:
    print("Base constraints UNSAT!")
    print("Need to debug...")