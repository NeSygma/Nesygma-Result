from z3 import *
solver = Solver()
# Birds and positions
birds = ['oyst','pet','rail','sand','tern']
pos = {b: Int(b) for b in birds}
for v in pos.values():
    solver.add(v >= 1, v <= 5)
solver.add(Distinct(list(pos.values())))
# Location per lecture position: True=Gladwyn, False=Howard
G = [Bool(f'G{i}') for i in range(1,6)]
# Base constraints
solver.add(G[0] == True)   # first Gladwyn
solver.add(G[3] == False)  # fourth Howard
solver.add(Sum([If(g,1,0) for g in G]) == 3)  # exactly three Gladwyn
# sandpipers Howard and earlier than oystercatchers
solver.add(G[pos['sand']-1] == False)
solver.add(pos['sand'] < pos['oyst'])
# petrels Gladwyn
solver.add(G[pos['pet']-1] == True)
# terns earlier than petrels
solver.add(pos['tern'] < pos['pet'])

# Options: we encode the falsity of each statement (i.e., the option being false)
# A: first and second both Gladwyn -> falsity: not (G1 and G2) => Or(Not(G1), Not(G2))
opt_a = Or(Not(G[0]), Not(G[1]))
# B: second and third both Howard -> falsity: not (not G2 and not G3) => Or(G2, G3)
opt_b = Or(G[1], G[2])
# C: second and fifth both Gladwyn -> falsity: Or(Not(G2), Not(G5))
opt_c = Or(Not(G[1]), Not(G[4]))
# D: third and fourth both Howard -> falsity: Or(G3, G4)
opt_d = Or(G[2], G[3])
# E: third and fifth both Gladwyn -> falsity: Or(Not(G3), Not(G5))
opt_e = Or(Not(G[2]), Not(G[4]))

options = [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]
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