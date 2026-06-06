from z3 import *

solver = Solver()

# Students: Franz(F), Greene(G), Hidalgo(H), Isaacs(I)
# Each has oil(O) and watercolor(W)
# 4 walls: 1,2,3,4; each wall has upper(0) and lower(1) position
# 8 paintings -> 8 slots (bijection)

# For each painting, assign a wall and a position
paintings = ['FO', 'FW', 'GO', 'GW', 'HO', 'HW', 'IO', 'IW']
wall = {p: Int(f'wall_{p}') for p in paintings}
pos = {p: Int(f'pos_{p}') for p in paintings}  # 0=upper, 1=lower

# Domain constraints
for p in paintings:
    solver.add(And(wall[p] >= 1, wall[p] <= 4))
    solver.add(Or(pos[p] == 0, pos[p] == 1))

# Bijection: all (wall, pos) pairs are distinct
all_pairs = [(wall[p], pos[p]) for p in paintings]
for i in range(len(all_pairs)):
    for j in range(i+1, len(all_pairs)):
        solver.add(Or(all_pairs[i][0] != all_pairs[j][0],
                       all_pairs[i][1] != all_pairs[j][1]))

# Constraint 1: No wall has only watercolors
# For each wall, at least one painting on it is oil
for w in range(1, 5):
    paintings_on_wall = [p for p in paintings]
    # At least one oil painting on wall w
    solver.add(Or([And(wall[p] == w, p[1] == 'O') for p in paintings]))

# Constraint 2: No wall has work of only one student
# For each wall, the two paintings must be by different students
students = {'F': ['FO', 'FW'], 'G': ['GO', 'GW'], 'H': ['HO', 'HW'], 'I': ['IO', 'IW']}
for w in range(1, 5):
    for s, ps in students.items():
        # Not both paintings of student s on wall w
        solver.add(Not(And(wall[ps[0]] == w, wall[ps[1]] == w)))

# Constraint 3: No wall has both Franz and Isaacs
for w in range(1, 5):
    for fp in ['FO', 'FW']:
        for ip in ['IO', 'IW']:
            solver.add(Not(And(wall[fp] == w, wall[ip] == w)))

# Constraint 4: Greene's watercolor is in upper position of wall where Franz's oil is
solver.add(wall['GW'] == wall['FO'])
solver.add(pos['GW'] == 0)

# Constraint 5: Isaacs's oil is in lower position of wall 4
solver.add(wall['IO'] == 4)
solver.add(pos['IO'] == 1)

# Additional condition: Greene's oil is on same wall as Franz's watercolor
solver.add(wall['GO'] == wall['FW'])

# Now check each answer choice
# (A) Greene's oil is displayed in an upper position
opt_a = (pos['GO'] == 0)
# (B) Hidalgo's watercolor is on same wall as Isaacs's watercolor
opt_b = (wall['HW'] == wall['IW'])
# (C) Hidalgo's oil is displayed in an upper position
opt_c = (pos['HO'] == 0)
# (D) Hidalgo's oil is on same wall as Isaacs's watercolor
opt_d = (wall['HO'] == wall['IW'])
# (E) Isaacs's watercolor is displayed in a lower position
opt_e = (pos['IW'] == 1)

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # Check if this MUST be true by checking if negation is unsat
    solver.add(Not(constr))
    result = solver.check()
    if result == unsat:
        found_options.append(letter)
    solver.pop()

print(f"Options that must be true: {found_options}")

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")