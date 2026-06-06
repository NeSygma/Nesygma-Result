from z3 import *
solver = Solver()

# Variables for each clue
R = Int('R')
S = Int('S')
T = Int('T')
U = Int('U')
W = Int('W')
X = Int('X')
Z = Int('Z')

# Domain constraints
solver.add(R >= 1, R <= 7)
solver.add(S >= 1, S <= 7)
solver.add(T >= 1, T <= 7)
solver.add(U >= 1, U <= 7)
solver.add(W >= 1, W <= 7)
solver.add(X >= 1, X <= 7)
solver.add(Z >= 1, Z <= 7)

# Distinctness
solver.add(Distinct(R, S, T, U, W, X, Z))

# U is in chapter 3
solver.add(U == 3)

# T cannot be in chapter 1
solver.add(T != 1)

# T before W and exactly two chapters between
solver.add(T < W)
solver.add(W - T == 3)

# S and Z not adjacent
solver.add(Abs(S - Z) != 1)

# W and X not adjacent
solver.add(Abs(W - X) != 1)

# U and X adjacent
solver.add(Abs(U - X) == 1)

# Option constraints
opt_a_constr = (R == 1)
opt_b_constr = (R == 5)
opt_c_constr = (S == 7)
opt_d_constr = (W == 6)
opt_e_constr = (X == 4)

found_options = []
for letter, constr in [('A', opt_a_constr), ('B', opt_b_constr), ('C', opt_c_constr), ('D', opt_d_constr), ('E', opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

if len(found_options) == 1:
    print('STATUS: sat')
    print('answer:' + found_options[0])
elif len(found_options) > 1:
    print('STATUS: unsat')
    print('Refine: Multiple options found ' + str(found_options))
else:
    print('STATUS: unsat')
    print('Refine: No options found')