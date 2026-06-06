from z3 import *

# singers
singers = ['K', 'L', 'T', 'W', 'Z', 'Y']
# position variables
pos = {s: Int(s) for s in singers}
solver = Solver()
# domain 1..6 and all distinct
for s in singers:
    solver.add(pos[s] >= 1, pos[s] <= 6)
solver.add(Distinct([pos[s] for s in singers]))
# recorded singers: K and L
# fourth audition cannot be recorded
solver.add(pos['K'] != 4, pos['L'] != 4)
# fifth audition must be recorded (either K or L)
solver.add(Or(pos['K'] == 5, pos['L'] == 5))
# Waite earlier than both recorded auditions
solver.add(pos['W'] < pos['K'])
solver.add(pos['W'] < pos['L'])
# Kammer earlier than Trillo
solver.add(pos['K'] < pos['T'])
# Zinn earlier than Yoshida
solver.add(pos['Z'] < pos['Y'])

# options constraints
options = []
# A: K sixth
options.append(("A", pos['K'] == 6))
# B: L sixth
options.append(("B", pos['L'] == 6))
# C: T sixth
options.append(("C", pos['T'] == 6))
# D: W sixth
options.append(("D", pos['W'] == 6))
# E: Z sixth
options.append(("E", pos['Z'] == 6))

found_options = []
for letter, constr in options:
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