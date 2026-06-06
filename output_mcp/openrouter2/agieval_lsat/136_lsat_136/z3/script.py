from z3 import *

solver = Solver()

# Variables
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')

hall_O = Bool('hall_O')
hall_P = Bool('hall_P')
hall_R = Bool('hall_R')
hall_S = Bool('hall_S')
hall_T = Bool('hall_T')

# Domain constraints
solver.add(pos_O >= 1, pos_O <= 5)
solver.add(pos_P >= 1, pos_P <= 5)
solver.add(pos_R >= 1, pos_R <= 5)
solver.add(pos_S >= 1, pos_S <= 5)
solver.add(pos_T >= 1, pos_T <= 5)

# Distinct positions
solver.add(Distinct(pos_O, pos_P, pos_R, pos_S, pos_T))

# First lecture in Gladwyn Hall
solver.add(Implies(pos_O == 1, hall_O == True))
solver.add(Implies(pos_P == 1, hall_P == True))
solver.add(Implies(pos_R == 1, hall_R == True))
solver.add(Implies(pos_S == 1, hall_S == True))
solver.add(Implies(pos_T == 1, hall_T == True))

# Fourth lecture in Howard Auditorium
solver.add(Implies(pos_O == 4, hall_O == False))
solver.add(Implies(pos_P == 4, hall_P == False))
solver.add(Implies(pos_R == 4, hall_R == False))
solver.add(Implies(pos_S == 4, hall_S == False))
solver.add(Implies(pos_T == 4, hall_T == False))

# Exactly three Gladwyn Hall
solver.add(Sum([If(hall_O, 1, 0), If(hall_P, 1, 0), If(hall_R, 1, 0), If(hall_S, 1, 0), If(hall_T, 1, 0)]) == 3)

# Sandpipers in Howard Auditorium
solver.add(hall_S == False)

# Sandpipers earlier than oystercatchers
solver.add(pos_S < pos_O)

# Terns earlier than petrels
solver.add(pos_T < pos_P)

# Petrels in Gladwyn Hall
solver.add(hall_P == True)

# Terns in Howard Auditorium (assumption)
solver.add(hall_T == False)

# Option constraints
opt_a_constr = And(pos_O == 3, hall_O == True)
opt_b_constr = And(pos_R == 3, hall_R == False)
opt_c_constr = And(pos_R == 3, hall_R == True)
opt_d_constr = And(pos_S == 3, hall_S == False)
opt_e_constr = And(pos_T == 3, hall_T == False)

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