from z3 import *

# Witnesses as Ints representing days: 0=Mon,1=Tue,2=Wed
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

witnesses = [Franco, Garcia, Hong, Iturbe, Jackson]

solver = Solver()
# Domain constraints
for w in witnesses:
    solver.add(And(w >= 0, w <= 2))

# Base constraints
solver.add(Franco != Garcia)  # Franco not same day as Garcia
solver.add(Iturbe == 2)       # Iturbe on Wednesday
solver.add(Sum([If(w == 1, 1, 0) for w in witnesses]) == 2)  # exactly two on Tuesday
solver.add(Hong != 0)         # Hong not on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in witnesses]) >= 1)  # at least one on Monday

# Option constraints
# A: Franco is the only witness on Monday
opt_a = And(
    Franco == 0,
    And([w != 0 for w in witnesses if w is not Franco])
)
# B: Franco same day as Iturbe
opt_b = Franco == Iturbe
# C: Garcia and Hong both on Tuesday
opt_c = And(Garcia == 1, Hong == 1)
# D: Garcia only on Monday, Hong on Wednesday, exactly two on Wednesday
opt_d = And(
    Garcia == 0,
    And([w != 0 for w in witnesses if w is not Garcia]),
    Hong == 2,
    Sum([If(w == 2, 1, 0) for w in witnesses]) == 2
)
# E: Jackson on Tuesday, exactly two on Monday
opt_e = And(
    Jackson == 1,
    Sum([If(w == 0, 1, 0) for w in witnesses]) == 2
)

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