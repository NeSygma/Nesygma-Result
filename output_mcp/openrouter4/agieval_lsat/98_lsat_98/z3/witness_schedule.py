from z3 import *

# Witnesses: Franco (F), Garcia (G), Hong (H), Iturbe (I), Jackson (J)
# Days: 0 = Monday, 1 = Tuesday, 2 = Wednesday

F, G, H, I, J = Ints('F G H I J')
witnesses = [F, G, H, I, J]
names = ['F', 'G', 'H', 'I', 'J']

solver = Solver()

# Each witness testifies on exactly one day (0, 1, or 2)
for w in witnesses:
    solver.add(w >= 0, w <= 2)

# Constraint 1: Franco does not testify on the same day as Garcia
solver.add(F != G)

# Constraint 2: Iturbe testifies on Wednesday (day 2)
solver.add(I == 2)

# Constraint 3: Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)

# Constraint 4: Hong does not testify on Monday (day 0)
solver.add(H != 0)

# Constraint 5: At least one witness testifies on Monday (day 0)
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)

# Now check each option
# Option A: Monday: Franco; Tuesday: Hong and Iturbe; Wednesday: Garcia and Jackson
# So: F=0, H=1, I=1, G=2, J=2
opt_a = And(F == 0, H == 1, I == 1, G == 2, J == 2)

# Option B: Monday: Franco and Hong; Tuesday: Iturbe and Jackson; Wednesday: Garcia
# So: F=0, H=0, I=1, J=1, G=2
opt_b = And(F == 0, H == 0, I == 1, J == 1, G == 2)

# Option C: Monday: Garcia; Tuesday: Franco and Iturbe; Wednesday: Hong and Jackson
# So: G=0, F=1, I=1, H=2, J=2
opt_c = And(G == 0, F == 1, I == 1, H == 2, J == 2)

# Option D: Monday: Garcia and Jackson; Tuesday: Franco and Hong; Wednesday: Iturbe
# So: G=0, J=0, F=1, H=1, I=2
opt_d = And(G == 0, J == 0, F == 1, H == 1, I == 2)

# Option E: Monday: Garcia and Jackson; Tuesday: Hong; Wednesday: Franco and Iturbe
# So: G=0, J=0, H=1, F=2, I=2
opt_e = And(G == 0, J == 0, H == 1, F == 2, I == 2)

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]

found_options = []
for letter, constr in options:
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