from z3 import *
solver = Solver()
# define bools
Myers = Bool('Myers')
Ortega = Bool('Ortega')
Paine = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong = Bool('Wong')
Yoder = Bool('Yoder')
Zayre = Bool('Zayre')

# base constraints
solver.add(Sum([If(Myers,1,0), If(Ortega,1,0), If(Paine,1,0), If(Schmidt,1,0), If(Thomson,1,0), If(Wong,1,0), If(Yoder,1,0), If(Zayre,1,0)]) >= 4)
solver.add(Implies(Myers, Not(Ortega)))
solver.add(Implies(Myers, Not(Paine)))
solver.add(Implies(Schmidt, Paine))
solver.add(Implies(Schmidt, Thomson))
solver.add(Implies(Wong, Myers))
solver.add(Implies(Wong, Yoder))
solver.add(Not(Yoder))

# options
opt_a_constr = Zayre
opt_b_constr = Thomson
opt_c_constr = Paine
opt_d_constr = Ortega
opt_e_constr = Myers

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