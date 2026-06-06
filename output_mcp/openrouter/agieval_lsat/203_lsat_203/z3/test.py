from z3 import *

singers = ['K','L','T','W','Y','Z']
# positions 1..6
pos = {name: Int(name) for name in singers}
solver = Solver()
# domain
for v in pos.values():
    solver.add(v >= 1, v <= 6)
# all different
solver.add(Distinct([pos[n] for n in singers]))
# Recorded: K and L
# fourth cannot be recorded
solver.add(pos['K'] != 4, pos['L'] != 4)
# fifth must be recorded
solver.add(Or(pos['K'] == 5, pos['L'] == 5))
# Waite earlier than both recorded
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])
# K earlier than T
solver.add(pos['K'] < pos['T'])
# Z earlier than Y
solver.add(pos['Z'] < pos['Y'])

# function to test option as second
options = {
    'A': 'K',
    'B': 'L',
    'C': 'T',
    'D': 'W',
    'E': 'Z'
}
found = []
for letter, name in options.items():
    solver.push()
    solver.add(pos[name] == 2)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()
print('Possible second options (SAT):', found)