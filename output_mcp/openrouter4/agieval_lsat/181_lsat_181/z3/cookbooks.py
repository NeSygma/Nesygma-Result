from z3 import *

solver = Solver()

# Boolean variables: True means fall, False means spring
K_f, L_f, M_f, N_f, O_f, P_f = Bools('K_f L_f M_f N_f O_f P_f')

# Constraint 1: M and P cannot be in the same season
solver.add(M_f != P_f)

# Constraint 2: K and N must be in the same season
solver.add(K_f == N_f)

# Constraint 3: If K is in fall, O must also be in fall
solver.add(Implies(K_f, O_f))

# Constraint 4: If M is in fall, N must be in spring
# M in fall => N not in fall (i.e., N in spring)
solver.add(Implies(M_f, Not(N_f)))

# Given condition: M is published in the fall
solver.add(M_f == True)

# Options
options = [
    ("A", K_f == True, O_f == True),   # K and O
    ("B", L_f == True, N_f == True),   # L and N
    ("C", L_f == True, O_f == True),   # L and O
    ("D", N_f == True, P_f == True),   # N and P
    ("E", O_f == True, P_f == True)    # O and P
]

found = []
for letter, constr1, constr2 in options:
    solver.push()
    solver.add(constr1)
    solver.add(constr2)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")