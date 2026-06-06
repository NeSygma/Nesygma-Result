from z3 import *

solver = Solver()

# Variables for each singer's audition position (1-6)
Kammer = Int('Kammer')
Lugo = Int('Lugo')
Trillo = Int('Trillo')
Waite = Int('Waite')
Yoshida = Int('Yoshida')
Zinn = Int('Zinn')

# Domain constraints
for v in [Kammer, Lugo, Trillo, Waite, Yoshida, Zinn]:
    solver.add(v >= 1, v <= 6)

# All auditions are at distinct positions
solver.add(Distinct(Kammer, Lugo, Trillo, Waite, Yoshida, Zinn))

# Recorded auditions: Kammer and Lugo
# 4th audition cannot be recorded
solver.add(Kammer != 4, Lugo != 4)
# 5th audition must be recorded
solver.add(Or(Kammer == 5, Lugo == 5))
# Waite's audition must take place earlier than the two recorded auditions
solver.add(Waite < Kammer, Waite < Lugo)
# Kammer's audition must take place earlier than Trillo's audition
solver.add(Kammer < Trillo)
# Zinn's audition must take place earlier than Yoshida's audition
solver.add(Zinn < Yoshida)

# Option constraints
opt_a_constr = (Yoshida == 5)
opt_b_constr = (Yoshida == 4)
opt_c_constr = (Yoshida == 3)
opt_d_constr = (Yoshida == 2)
opt_e_constr = (Yoshida == 1)

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