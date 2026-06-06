from z3 import *

solver = Solver()
# shelf indices: 0=bottom,1=middle,2=top
books = ['F','G','H','I','K','L','M','O']
vars = {b: Int(b) for b in books}
for b in books:
    solver.add(vars[b] >= 0, vars[b] <= 2)
# At least two books per shelf
for s in range(3):
    solver.add(Sum([If(vars[b] == s, 1, 0) for b in books]) >= 2)
# More books on bottom than top
bottom_cnt = Sum([If(vars[b] == 0, 1, 0) for b in books])
top_cnt = Sum([If(vars[b] == 2, 1, 0) for b in books])
solver.add(bottom_cnt > top_cnt)
# I on middle
solver.add(vars['I'] == 1)
# K higher than F
solver.add(vars['K'] > vars['F'])
# O higher than L
solver.add(vars['O'] > vars['L'])
# F same as M
solver.add(vars['F'] == vars['M'])
# Conditional premise: L higher than H
solver.add(vars['L'] > vars['H'])

# Option constraints
opt_a = vars['F'] == vars['G']
opt_b = vars['G'] == vars['H']
opt_c = vars['H'] == vars['M']
opt_d = vars['I'] == vars['G']
opt_e = vars['K'] == vars['O']

must_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
    solver.push()
    # add negation of the option; if unsat, then option must be true
    solver.add(Not(constr))
    if solver.check() == unsat:
        must_options.append(letter)
    solver.pop()

if len(must_options) == 1:
    print("STATUS: sat")
    print(f"answer:{must_options[0]}")
elif len(must_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple forced options {must_options}")
else:
    print("STATUS: unsat")
    print("Refine: No forced option found")