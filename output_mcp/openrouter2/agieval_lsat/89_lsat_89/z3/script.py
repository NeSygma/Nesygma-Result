from z3 import *

solver = Solver()

# Variables
wayne = [Bool(f"wayne_{i}") for i in range(5)]
trad = [Bool(f"trad_{i}") for i in range(5)]

# Base constraints
solver.add(trad[2] == True)

solver.add(Sum([If(trad[i], 1, 0) for i in range(5)]) == 2)

solver.add(Sum([If(And(trad[i], trad[i+1]), 1, 0) for i in range(4)]) == 1)

solver.add(wayne[3] == trad[3])

solver.add(wayne[1] != wayne[4])

for i in range(1,5):
    solver.add(Implies(trad[i], Or([And(wayne[j], Not(trad[j])) for j in range(i)])))

# Count of Wayne traditional solos
count = Sum([If(And(wayne[i], trad[i]), 1, 0) for i in range(5)])

# Option constraints
opt_a_constr = (count == 0)
opt_b_constr = (count == 1)
opt_c_constr = (count == 2)
opt_d_constr = (count == 3)
opt_e_constr = (count == 4)

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