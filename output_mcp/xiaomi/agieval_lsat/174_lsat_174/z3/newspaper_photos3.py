from z3 import *

solver = Solver()

# Sections: Lifestyle (L), Metro (M), Sports (S) - each has 2 photographs
# Photographers: Fuentes (0), Gagnon (1), Hue (2)
L = [Int(f'L_{i}') for i in range(2)]
M = [Int(f'M_{i}') for i in range(2)]
S = [Int(f'S_{i}') for i in range(2)]

# Domain constraints
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
solver.add(Or(
    And(L[0] == 0, Or(M[0] == 0, M[1] == 0)),
    And(L[0] == 1, Or(M[0] == 1, M[1] == 1)),
    And(L[0] == 2, Or(M[0] == 2, M[1] == 2)),
    And(L[1] == 0, Or(M[0] == 0, M[1] == 0)),
    And(L[1] == 1, Or(M[0] == 1, M[1] == 1)),
    And(L[1] == 2, Or(M[0] == 2, M[1] == 2)),
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

# Define options
# (A) Both photographs in the Lifestyle section are by Fuentes.
opt_a = And(L[0] == 0, L[1] == 0)

# (B) Both photographs in the Lifestyle section are by Gagnon.
opt_b = And(L[0] == 1, L[1] == 1)

# (C) One photograph in the Lifestyle section is by Gagnon and one is by Hue.
opt_c = Or(And(L[0] == 1, L[1] == 2), And(L[0] == 2, L[1] == 1))

# (D) Both photographs in the Lifestyle section are by Hue.
opt_d = And(L[0] == 2, L[1] == 2)

# (E) Both photographs in the Sports section are by Fuentes.
opt_e = And(S[0] == 0, S[1] == 0)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        m = solver.model()
        found_options.append(letter)
        print(f"Option {letter}: SAT")
        print(f"  L = [{m[L[0]]}, {m[L[1]]}]")
        print(f"  M = [{m[M[0]]}, {m[M[1]]}]")
        print(f"  S = [{m[S[0]]}, {m[S[1]]}]")
        print(f"  total_F = {m.eval(total_F)}, total_G = {m.eval(total_G)}, total_H = {m.eval(total_H)}")
    else:
        print(f"Option {letter}: UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")