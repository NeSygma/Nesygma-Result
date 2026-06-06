from z3 import *

# Declare position variables for each accomplice
Peters = Int('Peters')
Quinn = Int('Quinn')
Rovero = Int('Rovero')
Stanton = Int('Stanton')
Tao = Int('Tao')
Villas = Int('Villas')
White = Int('White')

solver = Solver()

# Domain constraints: positions 1-7, all distinct
all_positions = [Peters, Quinn, Rovero, Stanton, Tao, Villas, White]
for p in all_positions:
    solver.add(p >= 1, p <= 7)
solver.add(Distinct(all_positions))

# Base constraints from problem
# 1. Stanton was recruited neither immediately before nor immediately after Tao
solver.add(Not(Or(Stanton == Tao + 1, Stanton == Tao - 1)))

# 2. Quinn was recruited earlier than Rovero
solver.add(Quinn < Rovero)

# 3. Villas was recruited immediately before White
solver.add(Villas + 1 == White)

# 4. Peters was recruited fourth
solver.add(Peters == 4)

# Now define the options for middle five accomplices (positions 2-6)
# Each option is a list of 5 accomplices in order from position 2 to 6
options = {
    "A": ["Quinn", "Stanton", "Peters", "Tao", "Villas"],
    "B": ["Quinn", "Stanton", "Peters", "Tao", "White"],
    "C": ["Villas", "White", "Peters", "Quinn", "Stanton"],
    "D": ["Villas", "White", "Peters", "Rovero", "Stanton"],
    "E": ["Villas", "White", "Quinn", "Rovero", "Stanton"]
}

# Function to create constraint for an option
def option_constraint(option_list):
    # option_list is list of 5 accomplices for positions 2,3,4,5,6
    # We need to map each accomplice to its position
    constraints = []
    for i, accomplice in enumerate(option_list):
        pos = i + 2  # positions 2-6
        if accomplice == "Peters":
            constraints.append(Peters == pos)
        elif accomplice == "Quinn":
            constraints.append(Quinn == pos)
        elif accomplice == "Rovero":
            constraints.append(Rovero == pos)
        elif accomplice == "Stanton":
            constraints.append(Stanton == pos)
        elif accomplice == "Tao":
            constraints.append(Tao == pos)
        elif accomplice == "Villas":
            constraints.append(Villas == pos)
        elif accomplice == "White":
            constraints.append(White == pos)
    return And(constraints)

# Evaluate each option using the exact skeleton
found_options = []
for letter, opt_list in options.items():
    constr = option_constraint(opt_list)
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to requirements
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")