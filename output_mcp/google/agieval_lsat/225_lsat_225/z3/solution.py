from z3 import *
solver = Solver()

# Students: F, G, H, I
# Paintings: FO, FW, GO, GW, HO, HW, IO, IW
paintings = ['FO', 'FW', 'GO', 'GW', 'HO', 'HW', 'IO', 'IW']
walls = {p: Int(f'{p}_w') for p in paintings}
pos = {p: Int(f'{p}_p') for p in paintings}

for p in paintings:
    solver.add(walls[p] >= 1, walls[p] <= 4)
    solver.add(pos[p] >= 0, pos[p] <= 1)

for i in range(len(paintings)):
    for j in range(i + 1, len(paintings)):
        p1 = paintings[i]
        p2 = paintings[j]
        solver.add(Not(And(walls[p1] == walls[p2], pos[p1] == pos[p2])))

for w in range(1, 5):
    solver.add(Or([And(walls[p] == w, Or(p == 'FO', p == 'GO', p == 'HO', p == 'IO')) for p in paintings]))

for w in range(1, 5):
    students_on_w = []
    for s in ['F', 'G', 'H', 'I']:
        has_s = Or(walls[f'{s}O'] == w, walls[f'{s}W'] == w)
        students_on_w.append(If(has_s, 1, 0))
    solver.add(Sum(students_on_w) >= 2)

for w in range(1, 5):
    f_on_w = Or(walls['FO'] == w, walls['FW'] == w)
    i_on_w = Or(walls['IO'] == w, walls['IW'] == w)
    solver.add(Not(And(f_on_w, i_on_w)))

solver.add(walls['GW'] == walls['FO'])
solver.add(pos['GW'] == 0)
solver.add(pos['FO'] == 1)
solver.add(walls['IO'] == 4)
solver.add(pos['IO'] == 1)

# Options
opt_a_constr = (walls['FW'] == walls['GO'])
opt_b_constr = (walls['FW'] == walls['HO'])
opt_c_constr = (pos['GO'] == 0)
opt_d_constr = (pos['HW'] == 1)
opt_e_constr = (walls['IW'] == walls['HO'])

# We want to find which one CANNOT be true.
# So we check which one is UNSAT.
unsat_options = []
for letter, constr in [("A", opt_a_constr), ("B", opt_b_constr), ("C", opt_c_constr), ("D", opt_d_constr), ("E", opt_e_constr)]:
    solver.push()
    solver.add(constr)
    if solver.check() == unsat:
        unsat_options.append(letter)
    solver.pop()

if len(unsat_options) == 1:
    print("STATUS: sat")
    print(f"answer:{unsat_options[0]}")
elif len(unsat_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {unsat_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")