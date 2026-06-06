from z3 import *
solver = Solver()

# declare positions
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

# domain constraints
for v in [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]:
    solver.add(v >= 1, v <= 7)

# distinct positions
solver.add(Distinct([Peters, Quinn, Rovero, Stanton, Tao, Villas, White]))

# base constraints
solver.add(Peters == 4)
solver.add(White == Villas + 1)
solver.add(Quinn < Rovero)
solver.add(Not(Or(Stanton == Tao + 1, Tao == Stanton + 1)))

# option constraints
opt_a_constr = And(Quinn == 1, Tao == 2, Stanton == 3, Peters == 4, Villas == 5, White == 6, Rovero == 7)
opt_b_constr = And(Quinn == 1, White == 2, Rovero == 3, Peters == 4, Stanton == 5, Villas == 6, Tao == 7)
opt_c_constr = And(Villas == 1, White == 2, Quinn == 3, Stanton == 4, Peters == 5, Tao == 6, Rovero == 7)
opt_d_constr = And(Villas == 1, White == 2, Stanton == 3, Peters == 4, Quinn == 5, Tao == 6, Rovero == 7)
opt_e_constr = And(Villas == 1, White == 2, Stanton == 3, Peters == 4, Rovero == 5, Tao == 6, Quinn == 7)

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