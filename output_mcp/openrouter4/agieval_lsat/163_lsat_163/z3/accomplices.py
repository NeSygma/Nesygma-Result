from z3 import *

# Create variables for each person's position (1 to 7)
persons = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']
pos = {p: Int(p) for p in persons}

solver = Solver()

# All positions are between 1 and 7
for p in persons:
    solver.add(pos[p] >= 1, pos[p] <= 7)

# All positions are distinct
solver.add(Distinct([pos[p] for p in persons]))

# Constraint 1: Stanton was recruited neither immediately before nor immediately after Tao
# |pos(Stanton) - pos(Tao)| != 1
solver.add(Not(pos['Stanton'] - pos['Tao'] == 1))
solver.add(Not(pos['Tao'] - pos['Stanton'] == 1))

# Constraint 2: Quinn earlier than Rovero
solver.add(pos['Quinn'] < pos['Rovero'])

# Constraint 3: Villas immediately before White
solver.add(pos['Villas'] + 1 == pos['White'])

# Constraint 4: Peters fourth
solver.add(pos['Peters'] == 4)

# Now define the options as constraints on positions 2-6
# Each option is a list of 5 persons in order from position 2 to position 6
options = {
    "A": ['Quinn', 'Stanton', 'Peters', 'Tao', 'Villas'],
    "B": ['Quinn', 'Stanton', 'Peters', 'Tao', 'White'],
    "C": ['Villas', 'White', 'Peters', 'Quinn', 'Stanton'],
    "D": ['Villas', 'White', 'Peters', 'Rovero', 'Stanton'],
    "E": ['Villas', 'White', 'Quinn', 'Rovero', 'Stanton']
}

found_options = []

for letter, opt_list in options.items():
    solver.push()
    for idx, person in enumerate(opt_list, start=2):
        solver.add(pos[person] == idx)
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