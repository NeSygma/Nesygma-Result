from z3 import *

# Define shelves: 1=top,2=middle,3=bottom
books = ['F','G','H','I','K','L','M','O']
vars = {b: Int(b) for b in books}
solver = Solver()
# domain constraints
for v in vars.values():
    solver.add(And(v >= 1, v <= 3))
# at least two books per shelf
for s in [1,2,3]:
    solver.add(Sum([If(v == s, 1, 0) for v in vars.values()]) >= 2)
# more books on bottom than top
cnt_bottom = Sum([If(v == 3, 1, 0) for v in vars.values()])
cnt_top = Sum([If(v == 1, 1, 0) for v in vars.values()])
solver.add(cnt_bottom > cnt_top)
# I on middle
solver.add(vars['I'] == 2)
# K higher than F (higher = smaller number)
solver.add(vars['K'] < vars['F'])
# O higher than L
solver.add(vars['O'] < vars['L'])
# F same shelf as M
solver.add(vars['F'] == vars['M'])

# Option constraints
option_constraints = {
    'A': vars['I'] == vars['M'],
    'B': vars['K'] == vars['G'],
    'C': vars['L'] == vars['F'],
    'D': vars['M'] == vars['H'],
    'E': vars['H'] == vars['O'],
}

found_options = []
for letter, opt_constr in option_constraints.items():
    s = Solver()
    s.append(solver.assertions())
    s.add(opt_constr)
    if s.check() == sat:
        m = s.model()
        # blocking clause to see if another model exists
        block = []
        for b in books:
            v = vars[b]
            val = m.eval(v, model_completion=True)
            block.append(v != val)
        s2 = Solver()
        s2.append(solver.assertions())
        s2.add(opt_constr)
        s2.add(Or(block))
        if s2.check() == unsat:
            found_options.append(letter)
    # else unsat, ignore

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")