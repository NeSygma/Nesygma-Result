from z3 import *

# We have 7 positions (1-7) and 7 accomplices.
# Let's model each accomplice's position as an integer variable.
Peters, Quinn, Rovero, Stanton, Tao, Villas, White = Ints('Peters Quinn Rovero Stanton Tao Villas White')
accomplices = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
names = ["Peters", "Quinn", "Rovero", "Stanton", "Tao", "Villas", "White"]

solver = Solver()

# Domain: each position is between 1 and 7
for a in accomplices:
    solver.add(a >= 1, a <= 7)

# All distinct positions
solver.add(Distinct(accomplices))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao.
# i.e., |Stanton - Tao| != 1
solver.add(Not(Or(Stanton + 1 == Tao, Stanton - 1 == Tao)))

# Constraint 2: Quinn was recruited earlier than Rovero.
solver.add(Quinn < Rovero)

# Constraint 3: Villas was recruited immediately before White.
solver.add(Villas + 1 == White)

# Constraint 4: Peters was recruited fourth.
solver.add(Peters == 4)

# Now evaluate each option
# Each option gives a specific order from first (position 1) to last (position 7).
# We'll encode each option as a conjunction of assignments.

options = {
    "A": [("Quinn", 1), ("Tao", 2), ("Stanton", 3), ("Peters", 4), ("Villas", 5), ("White", 6), ("Rovero", 7)],
    "B": [("Quinn", 1), ("White", 2), ("Rovero", 3), ("Peters", 4), ("Stanton", 5), ("Villas", 6), ("Tao", 7)],
    "C": [("Villas", 1), ("White", 2), ("Quinn", 3), ("Stanton", 4), ("Peters", 5), ("Tao", 6), ("Rovero", 7)],
    "D": [("Villas", 1), ("White", 2), ("Stanton", 3), ("Peters", 4), ("Quinn", 5), ("Tao", 6), ("Rovero", 7)],
    "E": [("Villas", 1), ("White", 2), ("Stanton", 3), ("Peters", 4), ("Rovero", 5), ("Tao", 6), ("Quinn", 7)]
}

# Map name to Z3 variable
var_map = {"Peters": Peters, "Quinn": Quinn, "Rovero": Rovero, "Stanton": Stanton, "Tao": Tao, "Villas": Villas, "White": White}

found_options = []
for letter, assignments in options.items():
    solver.push()
    constr = And([var_map[name] == pos for name, pos in assignments])
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