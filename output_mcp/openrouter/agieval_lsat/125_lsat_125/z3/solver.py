from z3 import *

# Declare Bool variables for each employee
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

solver = Solver()
# Base constraints
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)  # at least 4 members
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))
solver.add(Implies(Schmidt, And(Paine, Thomson)))
solver.add(Implies(Wong, And(Myers, Yoder)))
# Given condition: Yoder not on team
solver.add(Not(Yoder))

# Option constraints: each option asserts that the employee is on the team
opt_a_constr = Zayre   # A
opt_b_constr = Thomson # B
opt_c_constr = Paine   # C
opt_d_constr = Ortega  # D
opt_e_constr = Myers   # E

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)  # require this employee to be on the team
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Determine which option is NOT possible (the EXCEPT answer)
all_options = {"A", "B", "C", "D", "E"}
impossible = list(all_options - set(found_options))
# Use impossible as the final answer set
found_options = impossible

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")