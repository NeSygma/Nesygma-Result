from z3 import *

solver = Solver()
articles = ['G','H','J','Q','R','S','Y']
pos = {a: Int(a) for a in articles}
# domain constraints
for a in articles:
    solver.add(pos[a] >= 1, pos[a] <= 7)
# all distinct
solver.add(Distinct([pos[a] for a in articles]))
# topic groups
finance = ['G','H','J']
nutrition = ['Q','R','S']
# consecutive same topic not allowed
for i in range(len(finance)):
    for j in range(i+1, len(finance)):
        solver.add(Abs(pos[finance[i]] - pos[finance[j]]) != 1)
for i in range(len(nutrition)):
    for j in range(i+1, len(nutrition)):
        solver.add(Abs(pos[nutrition[i]] - pos[nutrition[j]]) != 1)
# Additional constraints
# S earlier than Q only if Q is third: (S < Q) -> (Q == 3)
solver.add(Implies(pos['S'] < pos['Q'], pos['Q'] == 3))
# S earlier than Y
solver.add(pos['S'] < pos['Y'])
# J earlier than G, G earlier than R
solver.add(pos['J'] < pos['G'])
solver.add(pos['G'] < pos['R'])

options = [("A",1),("B",3),("C",4),("D",5),("E",6)]
impossible = []
for letter, p in options:
    solver.push()
    solver.add(pos['S'] == p)
    res = solver.check()
    if res == unsat:
        impossible.append(letter)
    solver.pop()

if len(impossible) == 1:
    print("STATUS: sat")
    print(f"answer:{impossible[0]}")
elif len(impossible) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple impossible options found {impossible}")
else:
    print("STATUS: unsat")
    print("Refine: No impossible options found")