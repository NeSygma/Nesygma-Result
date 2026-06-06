from z3 import *

solver = Solver()

# Position variables for each bird type (1..5)
pos_O = Int('pos_O')
pos_P = Int('pos_P')
pos_R = Int('pos_R')
pos_S = Int('pos_S')
pos_T = Int('pos_T')
positions = [pos_O, pos_P, pos_R, pos_S, pos_T]
for p in positions:
    solver.add(p >= 1, p <= 5)
solver.add(Distinct(positions))

# Location for each position: True = Gladwyn Hall (G), False = Howard Auditorium (H)
is_G = [Bool(f'is_G_{i}') for i in range(1,6)]  # index 0 -> position1
# First lecture in Gladwyn Hall
solver.add(is_G[0] == True)
# Fourth lecture in Howard Auditorium
solver.add(is_G[3] == False)
# Exactly three lectures in Gladwyn Hall
solver.add(Sum([If(is_G[i], 1, 0) for i in range(5)]) == 3)

# Location for each bird type
loc_O = Bool('loc_O')
loc_P = Bool('loc_P')
loc_R = Bool('loc_R')
loc_S = Bool('loc_S')
loc_T = Bool('loc_T')
locs = [loc_O, loc_P, loc_R, loc_S, loc_T]

# Link position to location via is_G at that position
for i in range(1,6):  # positions 1..5
    # For each bird type, if its position equals i, then its location equals is_G[i-1]
    solver.add(Implies(pos_O == i, loc_O == is_G[i-1]))
    solver.add(Implies(pos_P == i, loc_P == is_G[i-1]))
    solver.add(Implies(pos_R == i, loc_R == is_G[i-1]))
    solver.add(Implies(pos_S == i, loc_S == is_G[i-1]))
    solver.add(Implies(pos_T == i, loc_T == is_G[i-1]))

# Specific constraints from the problem
# Sandpipers in Howard Auditorium
solver.add(loc_S == False)
# Sandpipers earlier than Oystercatchers
solver.add(pos_S < pos_O)
# Petrels in Gladwyn Hall
solver.add(loc_P == True)
# Terns earlier than Petrels
solver.add(pos_T < pos_P)

# Define option constraints
options = {
    "A": [pos_O == 5, is_G[4] == True],
    "B": [pos_P == 5, is_G[4] == False],
    "C": [pos_R == 5, is_G[4] == False],
    "D": [pos_S == 5, is_G[4] == False],
    "E": [pos_T == 5, is_G[4] == True]
}

found_options = []
for letter, constrs in options.items():
    solver.push()
    for c in constrs:
        solver.add(c)
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