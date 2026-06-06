from z3 import *

solver = Solver()
# Variables: position of each bird (1..5)
birds = ['oyst','pet','rail','sand','tern']
pos = {b: Int(b) for b in birds}
for v in pos.values():
    solver.add(v >= 1, v <= 5)
solver.add(Distinct(list(pos.values())))
# Location per lecture position: True = Gladwyn, False = Howard
G = [Bool(f'G{i}') for i in range(1,6)]  # G1..G5
# Base constraints
solver.add(G[0] == True)   # first lecture Gladwyn
solver.add(G[3] == False)  # fourth lecture Howard
solver.add(Sum([If(g,1,0) for g in G]) == 3)  # exactly three Gladwyn
# sandpipers in Howard and earlier than oystercatchers
solver.add(Implies(pos['sand'] == 1, G[0] == False))
solver.add(Implies(pos['sand'] == 2, G[1] == False))
solver.add(Implies(pos['sand'] == 3, G[2] == False))
solver.add(Implies(pos['sand'] == 4, G[3] == False))
solver.add(Implies(pos['sand'] == 5, G[4] == False))
solver.add(pos['sand'] < pos['oyst'])
# petrels in Gladwyn
for i in range(5):
    solver.add(Implies(pos['pet'] == i+1, G[i] == True))
# terns earlier than petrels
solver.add(pos['tern'] < pos['pet'])

# Define negated option constraints (option is false)
opt_a = Or(Not(G[0]), Not(G[1]))                     # not both first and second Gladwyn
opt_b = Or(G[1], G[2])                               # not both second and third Howard (i.e., at least one Gladwyn)
opt_c = Or(Not(G[1]), Not(G[4]))                     # not both second and fifth Gladwyn
opt_d = Or(G[2], G[3])                               # not both third and fourth Howard
opt_e = Or(Not(G[2]), Not(G[4]))                     # not both third and fifth Gladwyn

options = [
    ("A", opt_a),
    ("B", opt_b),
    ("C", opt_c),
    ("D", opt_d),
    ("E", opt_e)
]

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