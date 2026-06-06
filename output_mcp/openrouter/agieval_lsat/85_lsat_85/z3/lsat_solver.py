from z3 import *

# Define persons
persons = ['Kim', 'Mahr', 'Parra', 'Quinn', 'Stuckey', 'Tiao', 'Udall']
vars = {p: Int(p) for p in persons}
solver = Solver()
# Domain constraints: each in {1,2,3}
for v in vars.values():
    solver.add(v >= 1, v <= 3)
# Base constraints
# Parra or Tiao (but not both) in Zone1
solver.add(Or(vars['Parra'] == 1, vars['Tiao'] == 1))
solver.add(Not(And(vars['Parra'] == 1, vars['Tiao'] == 1)))
# Tiao or Udall (but not both) in Zone2
solver.add(Or(vars['Tiao'] == 2, vars['Udall'] == 2))
solver.add(Not(And(vars['Tiao'] == 2, vars['Udall'] == 2)))
# Parra and Quinn same zone
solver.add(vars['Parra'] == vars['Quinn'])
# Stuckey and Udall same zone
solver.add(vars['Stuckey'] == vars['Udall'])
# More in Zone3 than Zone2
zone3 = Sum([If(v == 3, 1, 0) for v in vars.values()])
zone2 = Sum([If(v == 2, 1, 0) for v in vars.values()])
solver.add(zone3 > zone2)

# Define option constraints
options = {
    'A': ['Kim', 'Mahr'],
    'B': ['Kim', 'Tiao'],
    'C': ['Parra', 'Quinn'],
    'D': ['Stuckey', 'Tiao', 'Udall'],
    'E': ['Parra', 'Quinn', 'Stuckey', 'Udall']
}

opt_constraints = {}
for letter, lst in options.items():
    cons = []
    for p in persons:
        if p in lst:
            cons.append(vars[p] == 3)
        else:
            cons.append(vars[p] != 3)
    opt_constraints[letter] = And(cons)

found_options = []
for letter, constr in [(l, opt_constraints[l]) for l in ['A','B','C','D','E']]:
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