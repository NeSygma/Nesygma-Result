from z3 import *

solver = Solver()
# Witness variables: 0=Mon,1=Tue,2=Wed
Franco = Int('Franco')
Garcia = Int('Garcia')
Hong = Int('Hong')
Iturbe = Int('Iturbe')
Jackson = Int('Jackson')

# Domain constraints
for w in [Franco, Garcia, Hong, Iturbe, Jackson]:
    solver.add(w >= 0, w <= 2)

# Base constraints
solver.add(Franco != Garcia)  # Franco does not testify on same day as Garcia
solver.add(Iturbe == 2)       # Iturbe testifies on Wednesday
# Exactly two witnesses testify on Tuesday (day 1)
solver.add(Sum([If(w == 1, 1, 0) for w in [Franco, Garcia, Hong, Iturbe, Jackson]]) == 2)
solver.add(Hong != 0)         # Hong does not testify on Monday
solver.add(Sum([If(w == 0, 1, 0) for w in [Franco, Garcia, Hong, Iturbe, Jackson]]) >= 1)  # At least one on Monday

# Option constraints
opt_a_constr = And(
    Franco == 0,
    Hong == 1,
    Iturbe == 1,
    Garcia == 2,
    Jackson == 2
)
opt_b_constr = And(
    Franco == 0,
    Hong == 0,
    Iturbe == 1,
    Jackson == 1,
    Garcia == 2
)
opt_c_constr = And(
    Garcia == 0,
    Franco == 1,
    Iturbe == 1,
    Hong == 2,
    Jackson == 2
)
opt_d_constr = And(
    Garcia == 0,
    Jackson == 0,
    Franco == 1,
    Hong == 1,
    Iturbe == 2
)
opt_e_constr = And(
    Garcia == 0,
    Jackson == 0,
    Hong == 1,
    Franco == 2,
    Iturbe == 2
)

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
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