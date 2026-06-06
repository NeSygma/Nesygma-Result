from z3 import *

# Variables for each book's shelf: 1=top,2=middle,3=bottom
books = ['F','G','H','I','K','L','M','O']
vars = {b: Int(b) for b in books}
solver = Solver()
# domain constraints
for v in vars.values():
    solver.add(v >= 1, v <= 3)
# at least two per shelf
for s in [1,2,3]:
    solver.add(Sum([If(v == s, 1, 0) for v in vars.values()]) >= 2)
# bottom > top
bottom = Sum([If(v == 3, 1, 0) for v in vars.values()])
top = Sum([If(v == 1, 1, 0) for v in vars.values()])
solver.add(bottom > top)
# specific constraints
solver.add(vars['I'] == 2)  # middle
solver.add(vars['K'] < vars['F'])  # higher shelf means smaller number
solver.add(vars['O'] < vars['L'])
solver.add(vars['F'] == vars['M'])

# Define options as constraints
opt_a = vars['O'] < vars['M']
opt_b = vars['K'] < vars['G']
opt_c = vars['I'] < vars['F']
opt_d = vars['G'] < vars['O']
opt_e = vars['F'] < vars['L']

found_options = []
for letter, constr in [("A", opt_a), ("B", opt_b), ("C", opt_c), ("D", opt_d), ("E", opt_e)]:
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