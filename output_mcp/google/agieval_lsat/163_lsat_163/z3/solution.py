from z3 import *

# Accomplices: P, Q, R, S, T, V, W
# Positions: 1, 2, 3, 4, 5, 6, 7
# P = 4
# V, W are adjacent (V, W) -> pos(W) = pos(V) + 1
# Q < R
# |pos(S) - pos(T)| != 1

# Define variables for positions of each accomplice
# pos_P, pos_Q, pos_R, pos_S, pos_T, pos_V, pos_W
pos = {name: Int(name) for name in ['P', 'Q', 'R', 'S', 'T', 'V', 'W']}

solver = Solver()

# Domain constraints
for name in pos:
    solver.add(pos[name] >= 1, pos[name] <= 7)

# All positions are distinct
solver.add(Distinct([pos[name] for name in pos]))

# P is 4th
solver.add(pos['P'] == 4)

# V is immediately before W
solver.add(pos['W'] == pos['V'] + 1)

# Q is earlier than R
solver.add(pos['Q'] < pos['R'])

# S is not immediately before or after T
solver.add(Abs(pos['S'] - pos['T']) > 1)

# Define the options for positions 2, 3, 4, 5, 6
# Option format: (pos2, pos3, pos4, pos5, pos6)
# Note: pos4 must be P (which is 4)
options = {
    "A": ["Q", "S", "P", "T", "V"],
    "B": ["Q", "S", "P", "T", "W"],
    "C": ["V", "W", "P", "Q", "S"],
    "D": ["V", "W", "P", "R", "S"],
    "E": ["V", "W", "Q", "R", "S"]
}

found_options = []

for letter, names in options.items():
    solver.push()
    # Add constraints for the option
    # names[0] is at pos 2, names[1] at pos 3, names[2] at pos 4, names[3] at pos 5, names[4] at pos 6
    solver.add(pos[names[0]] == 2)
    solver.add(pos[names[1]] == 3)
    solver.add(pos[names[2]] == 4)
    solver.add(pos[names[3]] == 5)
    solver.add(pos[names[4]] == 6)
    
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