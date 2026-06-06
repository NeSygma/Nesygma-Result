from z3 import *

solver = Solver()

# Bool variables for each employee
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

employees = [Myers, Ortega, Paine, Schmidt, Thomson, Wong, Yoder, Zayre]

# At least four employees on the team
solver.add(Sum([If(e, 1, 0) for e in employees]) >= 4)

# Constraints from the problem
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))
solver.add(Implies(Schmidt, And(Paine, Thomson)))
solver.add(Implies(Wong, And(Myers, Yoder)))

# Option constraints: both members of the pair are NOT on the team
opt_a_constr = And(Not(Ortega), Not(Schmidt))   # A: Ortega and Schmidt
opt_b_constr = And(Not(Ortega), Not(Wong))      # B: Ortega and Wong
opt_c_constr = And(Not(Paine), Not(Schmidt))   # C: Paine and Schmidt
opt_d_constr = And(Not(Thomson), Not(Yoder))   # D: Thomson and Yoder
opt_e_constr = And(Not(Yoder), Not(Zayre))     # E: Yoder and Zayre

found_options = []
results = {}
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    res = solver.check()
    results[letter] = res
    if res == sat:
        found_options.append(letter)
    solver.pop()

# Options that make the problem UNSAT (both not on team leads to contradiction)
unsat_options = [letter for letter, res in results.items() if res == unsat]
# Use unsat_options as the decisive list per problem requirement
found_options = unsat_options

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")