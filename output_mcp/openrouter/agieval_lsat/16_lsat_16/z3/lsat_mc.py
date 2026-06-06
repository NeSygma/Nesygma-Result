from z3 import *

solver = Solver()
# compositions
comps = ['F','H','L','O','P','R','S','T']
pos = {c: Int(c) for c in comps}
# domain 1..8
for c in comps:
    solver.add(pos[c] >= 1, pos[c] <= 8)
# all distinct
solver.add(Distinct([pos[c] for c in comps]))
# base constraints
# 1. T either immediately before F or immediately after R
solver.add(Or(pos['T'] + 1 == pos['F'], pos['T'] == pos['R'] + 1))
# 2. at least two compositions between F and R => |posF - posR| >= 3
solver.add(Or(pos['F'] - pos['R'] >= 3, pos['R'] - pos['F'] >= 3))
# 3. O first or fifth
solver.add(Or(pos['O'] == 1, pos['O'] == 5))
# 4. eighth is L or H
solver.add(Or(pos['L'] == 8, pos['H'] == 8))
# 5. P before S
solver.add(pos['P'] < pos['S'])
# 6. at least one composition between O and S => |posO - posS| >= 2
solver.add(Or(pos['O'] - pos['S'] >= 2, pos['S'] - pos['O'] >= 2))
# Question condition: S is fourth
solver.add(pos['S'] == 4)

# Define option constraints
opt_constraints = {}
# A: F, H, P first three
opt_constraints['A'] = And(pos['F'] == 1, pos['H'] == 2, pos['P'] == 3)
# B: H, P, L
opt_constraints['B'] = And(pos['H'] == 1, pos['P'] == 2, pos['L'] == 3)
# C: O, P, R
opt_constraints['C'] = And(pos['O'] == 1, pos['P'] == 2, pos['R'] == 3)
# D: O, P, T
opt_constraints['D'] = And(pos['O'] == 1, pos['P'] == 2, pos['T'] == 3)
# E: P, R, T
opt_constraints['E'] = And(pos['P'] == 1, pos['R'] == 2, pos['T'] == 3)

found_options = []
for letter, constr in [('A', opt_constraints['A']), ('B', opt_constraints['B']), ('C', opt_constraints['C']), ('D', opt_constraints['D']), ('E', opt_constraints['E'])]:
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