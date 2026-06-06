from z3 import *

solver = Solver()

# Declare variables for each cargo's bay number
G = Int('grain')
L = Int('livestock')
T = Int('textiles')
P = Int('produce')
F = Int('fuel')
M = Int('machinery')

# All variables are between 1 and 6
solver.add(G >= 1, G <= 6)
solver.add(L >= 1, L <= 6)
solver.add(T >= 1, T <= 6)
solver.add(P >= 1, P <= 6)
solver.add(F >= 1, F <= 6)
solver.add(M >= 1, M <= 6)

# All distinct
solver.add(Distinct(G, L, T, P, F, M))

# Constraints
solver.add(G > L)
solver.add(L > T)
solver.add(P > F)
solver.add(Or(T - P == 1, P - T == 1))  # |T - P| = 1

# Now test each option: which cargo cannot be in bay 4?
# We'll test by adding constraint that the cargo's bay is 4, and check if unsat.
found_options = []
for letter, constr in [
    ("A", G == 4),
    ("B", L == 4),
    ("C", M == 4),
    ("D", P == 4),
    ("E", T == 4)
]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
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