from z3 import *

solver = Solver()
articles = ['G','H','J','Q','R','S','Y']
pos = {a: Int(a) for a in articles}
# domain
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
# distinct
solver.add(Distinct([pos[a] for a in articles]))
# topic groups
finance = ['G','H','J']
nutrition = ['Q','R','S']
# consecutive same topic not allowed
for a in finance:
    for b in finance:
        if a < b:
            solver.add(Abs(pos[a] - pos[b]) != 1)
for a in nutrition:
    for b in nutrition:
        if a < b:
            solver.add(Abs(pos[a] - pos[b]) != 1)
# Additional constraints
# S earlier than Q only if Q is third: (S < Q) -> (Q == 3)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
# S earlier than Y
solver.add(pos['S'] < pos['Y'])
# J earlier than G, G earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

options = [("A",1),("B",3),("C",4),("D",5),("E",6)]
found = []
for letter, p in options:
    solver.push()
    solver.add(pos['S'] == p)
    if solver.check() == sat:
        found.append(letter)
    solver.pop()

if len(found) == 1:
    print("STATUS: sat")
    print(f"answer:{found[0]}")
elif len(found) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")