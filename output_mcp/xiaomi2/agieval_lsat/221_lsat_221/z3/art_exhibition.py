from z3 import *

solver = Solver()

# Paintings: 0=FO, 1=FW, 2=GO, 3=GW, 4=HO, 5=HW, 6=IO, 7=IW
# Walls: 0=wall1, 1=wall2, 2=wall3, 3=wall4
# Positions: 0=upper, 1=lower

N = 8  # number of paintings
W = 4  # number of walls

wall = [Int(f'wall_{p}') for p in range(N)]
pos = [Int(f'pos_{p}') for p in range(N)]

# Each painting on exactly one wall (0-3) with position (0=upper, 1=lower)
for p in range(N):
    solver.add(wall[p] >= 0, wall[p] < W)
    solver.add(Or(pos[p] == 0, pos[p] == 1))

# All (wall, pos) pairs are distinct — each wall has exactly one upper and one lower
# Encode as wall[p]*2 + pos[p], giving values 0-7, all distinct
assignment = [wall[p] * 2 + pos[p] for p in range(N)]
solver.add(Distinct(assignment))

# Constraint 1: No wall has only watercolors (at least one oil per wall)
# Oil paintings: 0(FO), 2(GO), 4(HO), 6(IO)
for w in range(W):
    solver.add(Or([wall[p] == w for p in [0, 2, 4, 6]]))

# Constraint 2: No wall has work of only one student
# Students: F={0,1}, G={2,3}, H={4,5}, I={6,7}
students = [(0,1), (2,3), (4,5), (6,7)]
for w in range(W):
    for s_p1, s_p2 in students:
        solver.add(Not(And(wall[s_p1] == w, wall[s_p2] == w)))

# Constraint 3: No wall has both a Franz painting and an Isaacs painting
# Franz: {0,1}, Isaacs: {6,7}
for w in range(W):
    for fp in [0, 1]:
        for ip in [6, 7]:
            solver.add(Not(And(wall[fp] == w, wall[ip] == w)))

# Constraint 4: Greene's watercolor (3) is upper on the wall where Franz's oil (0) is
solver.add(wall[3] == wall[0])
solver.add(pos[3] == 0)  # GW is upper
solver.add(pos[0] == 1)  # FO is lower

# Constraint 5: Isaacs's oil (6) is lower on wall 4 (index 3)
solver.add(wall[6] == 3)
solver.add(pos[6] == 1)

# Given: Hidalgo's oil (4) is on wall 2 (index 1)
solver.add(wall[4] == 1)

# Test each option: what else could be on wall 2 (index 1)?
options = [
    ("A", wall[0] == 1),  # Franz's oil
    ("B", wall[3] == 1),  # Greene's watercolor
    ("C", wall[2] == 1),  # Greene's oil
    ("D", wall[5] == 1),  # Hidalgo's watercolor
    ("E", wall[7] == 1),  # Isaacs's watercolor
]

found_options = []
for letter, constr in options:
    solver.push()
    solver.add(constr)
    result = solver.check()
    if result == sat:
        found_options.append(letter)
        m = solver.model()
        print(f"Option {letter} is SAT:")
        for p in range(N):
            w_val = m.evaluate(wall[p])
            p_val = m.evaluate(pos[p])
            names = ["FO","FW","GO","GW","HO","HW","IO","IW"]
            print(f"  {names[p]} -> wall {int(str(w_val))+1}, {'upper' if int(str(p_val))==0 else 'lower'}")
    else:
        print(f"Option {letter} is UNSAT")
    solver.pop()

print()
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")