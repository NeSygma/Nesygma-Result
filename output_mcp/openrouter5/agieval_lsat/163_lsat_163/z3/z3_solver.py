from z3 import *

solver = Solver()

# 7 accomplices: Peters, Quinn, Rovero, Stanton, Tao, Villas, White
# Positions 1 through 7 (1 = first recruited, 7 = last recruited)
# We'll use Int variables for each person's position

Peters, Quinn, Rovero, Stanton, Tao, Villas, White = Ints('Peters Quinn Rovero Stanton Tao Villas White')
persons = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]

# Each position is between 1 and 7
for p in persons:
    solver.add(p >= 1, p <= 7)

# All positions are distinct
solver.add(Distinct(persons))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao.
# |Stanton - Tao| != 1
solver.add(Not(Or(Stanton + 1 == Tao, Stanton - 1 == Tao)))

# Constraint 2: Quinn was recruited earlier than Rovero.
solver.add(Quinn < Rovero)

# Constraint 3: Villas was recruited immediately before White.
solver.add(Villas + 1 == White)

# Constraint 4: Peters was recruited fourth.
solver.add(Peters == 4)

# Now evaluate each option.
# Each option gives the order of the middle five (positions 2 through 6).
# So we need to constrain positions 2,3,4,5,6 to match the given order.

# Option A: Quinn, Stanton, Peters, Tao, Villas
# Position 2=Quinn, 3=Stanton, 4=Peters, 5=Tao, 6=Villas
opt_a_constr = And(
    Quinn == 2,
    Stanton == 3,
    Peters == 4,
    Tao == 5,
    Villas == 6
)

# Option B: Quinn, Stanton, Peters, Tao, White
# Position 2=Quinn, 3=Stanton, 4=Peters, 5=Tao, 6=White
opt_b_constr = And(
    Quinn == 2,
    Stanton == 3,
    Peters == 4,
    Tao == 5,
    White == 6
)

# Option C: Villas, White, Peters, Quinn, Stanton
# Position 2=Villas, 3=White, 4=Peters, 5=Quinn, 6=Stanton
opt_c_constr = And(
    Villas == 2,
    White == 3,
    Peters == 4,
    Quinn == 5,
    Stanton == 6
)

# Option D: Villas, White, Peters, Rovero, Stanton
# Position 2=Villas, 3=White, 4=Peters, 5=Rovero, 6=Stanton
opt_d_constr = And(
    Villas == 2,
    White == 3,
    Peters == 4,
    Rovero == 5,
    Stanton == 6
)

# Option E: Villas, White, Quinn, Rovero, Stanton
# Position 2=Villas, 3=White, 4=Quinn, 5=Rovero, 6=Stanton
opt_e_constr = And(
    Villas == 2,
    White == 3,
    Quinn == 4,
    Rovero == 5,
    Stanton == 6
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