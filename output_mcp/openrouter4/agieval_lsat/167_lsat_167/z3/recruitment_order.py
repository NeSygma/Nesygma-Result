from z3 import *

solver = Solver()

# Persons Peters, Quinn, Rovero, Stanton, Tao, Villas, White
P = Int('Peters')
Q = Int('Quinn')
R = Int('Rovero')
S = Int('Stanton')
T = Int('Tao')
V = Int('Villas')
W = Int('White')

persons = [P, Q, R, S, T, V, W]

# Domain: positions 1 through 7
for p in persons:
    solver.add(p >= 1, p <= 7)

# All distinct positions
solver.add(Distinct(persons))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
# Not (S + 1 == T) and not (S - 1 == T)
solver.add(Not(S + 1 == T))
solver.add(Not(S - 1 == T))

# Constraint 2: Quinn was recruited earlier than Rovero
solver.add(Q < R)

# Constraint 3: Villas was recruited immediately before White
solver.add(V + 1 == W)

# Constraint 4: Peters was recruited fourth
solver.add(P == 4)

# Additional condition (Q premise): White was recruited immediately before Quinn
solver.add(W + 1 == Q)

# Now evaluate each option: which one must be sixth?
options = {
    "A": Q,  # Quinn is sixth
    "B": R,  # Rovero is sixth
    "C": S,  # Stanton is sixth
    "D": V,  # Villas is sixth
    "E": W   # White is sixth
}

found_options = []

for letter, var in options.items():
    solver.push()
    solver.add(var == 6)
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