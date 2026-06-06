from z3 import *

# Define positions 1..7 for each person
persons = ['Peters', 'Quinn', 'Rovero', 'Stanton', 'Tao', 'Villas', 'White']
pos = {name: Int(name) for name in persons}
solver = Solver()

# Domain constraints: positions 1..7
for p in persons:
    solver.add(pos[p] >= 1, pos[p] <= 7)
# All-different
solver.add(Distinct([pos[p] for p in persons]))

# Base constraints
solver.add(pos['Peters'] == 4)                     # Peters fourth
solver.add(pos['Villas'] + 1 == pos['White'])      # Villas immediately before White
solver.add(pos['Quinn'] < pos['Rovero'])           # Quinn earlier than Rovero
# Stanton not immediately before nor after Tao
solver.add(Abs(pos['Stanton'] - pos['Tao']) != 1)
# Additional condition for the question: Quinn immediately before Rovero
solver.add(pos['Quinn'] + 1 == pos['Rovero'])

# Mapping options to positions
option_map = {
    'A': 1,  # first
    'B': 2,  # second
    'C': 3,  # third
    'D': 5,  # fifth
    'E': 7   # seventh
}

found_options = []
for letter, position in option_map.items():
    solver.push()
    solver.add(pos['Stanton'] == position)
    if solver.check() == unsat:
        # This option leads to contradiction, i.e., Stanton cannot be at this position
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