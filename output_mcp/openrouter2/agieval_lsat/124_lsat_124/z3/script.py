from z3 import *

# Declare boolean variables for each employee
Myers   = Bool('Myers')
Ortega  = Bool('Ortega')
Paine   = Bool('Paine')
Schmidt = Bool('Schmidt')
Thomson = Bool('Thomson')
Wong    = Bool('Wong')
Yoder   = Bool('Yoder')
Zayre   = Bool('Zayre')

# Base constraints
solver = Solver()

# At least four employees must be selected
solver.add(Sum([If(Myers, 1, 0), If(Ortega, 1, 0), If(Paine, 1, 0),
                If(Schmidt, 1, 0), If(Thomson, 1, 0), If(Wong, 1, 0),
                If(Yoder, 1, 0), If(Zayre, 1, 0)]) >= 4)

# Conditional constraints
solver.add(Implies(Myers, And(Not(Ortega), Not(Paine))))
solver.add(Implies(Schmidt, And(Paine, Thomson)))
solver.add(Implies(Wong, And(Myers, Yoder)))

# Option constraints
opt_a_constr = And(Myers, Thomson)          # (A) Myers and Thomson
opt_b_constr = And(Ortega, Yoder)           # (B) Ortega and Yoder
opt_c_constr = And(Paine, Zayre)            # (C) Paine and Zayre
opt_d_constr = And(Schmidt, Wong)          # (D) Schmidt and Wong
opt_e_constr = And(Wong, Yoder)             # (E) Wong and Yoder

found_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr),
                       ("C", opt_c_constr), ("D", opt_d_constr),
                       ("E", opt_e_constr)]:
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