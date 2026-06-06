from z3 import *

# Define positions 1..6 for each member
members = ['G','K','P','S','T','V']
pos = {m: Int(m) for m in members}
solver = Solver()
# domain constraints
for m in members:
    solver.add(pos[m] >= 1, pos[m] <= 6)
# all distinct
solver.add(Distinct([pos[m] for m in members]))
# base constraints
solver.add(pos['G'] != 4)                     # guitarist not 4th
solver.add(pos['P'] < pos['K'])               # percussionist before keyboard
solver.add(pos['V'] < pos['K'], pos['K'] < pos['G'])  # violinist before keyboard before guitarist
# saxophonist after either percussionist or trumpeter but not both (xor)
# exclusive or: (S > P) != (S > T) and at least one true
cond1 = pos['S'] > pos['P']
cond2 = pos['S'] > pos['T']
solver.add(Or(cond1, cond2))
solver.add(cond1 != cond2)
# premise: percussionist before saxophonist
solver.add(pos['P'] < pos['S'])

# Define option conditions (the statement that must be true)
opt_A = pos['P'] == 1
opt_B = pos['P'] == 2
opt_C = pos['V'] < pos['S']
opt_D = pos['P'] < pos['T']
opt_E = pos['S'] < pos['K']
options = [
    ("A", opt_A),
    ("B", opt_B),
    ("C", opt_C),
    ("D", opt_D),
    ("E", opt_E)
]

forced = []
for letter, cond in options:
    # check if the negation of the condition is impossible (unsat)
    solver.push()
    solver.add(Not(cond))
    res = solver.check()
    if res == unsat:
        forced.append(letter)
    solver.pop()

if len(forced) == 1:
    print("STATUS: sat")
    print(f"answer:{forced[0]}")
else:
    # For debugging, list possibilities
    print("STATUS: unsat")
    print(f"Forced options found: {forced}")