from z3 import *

# Employees
names = ['Robertson','Souza','Togowa','Vaughn','Xu','Young']
# Create Int variables for parking spaces 1..6
vars = {n: Int(n) for n in names}

base_solver = Solver()
# Domain constraints
for v in vars.values():
    base_solver.add(v >= 1, v <= 6)
# All different
base_solver.add(Distinct(list(vars.values())))
# Ordering constraints
base_solver.add(vars['Young'] > vars['Togowa'])
base_solver.add(vars['Xu'] > vars['Souza'])
base_solver.add(vars['Robertson'] > vars['Young'])
# Robertson limited to 1-4
base_solver.add(Or([vars['Robertson'] == i for i in range(1,5)]))

# Enumerate all solutions to compute possible spaces per employee
possible = {n: set() for n in names}
enum_solver = Solver()
enum_solver.append(base_solver.assertions())
while enum_solver.check() == sat:
    m = enum_solver.model()
    for n in names:
        possible[n].add(m[vars[n]].as_long())
    # block this solution
    block = []
    for n in names:
        block.append(vars[n] != m[vars[n]])
    enum_solver.add(Or(block))

# Count employees with exactly two possible spaces
num_two = sum(1 for s in possible.values() if len(s) == 2)

# Prepare options
options = [
    ("A", 0),
    ("B", 2),
    ("C", 3),
    ("D", 4),
    ("E", 5)
]

found_options = []
for letter, target in options:
    solver = Solver()
    solver.append(base_solver.assertions())
    # add constraint that num_two equals target
    solver.add(BoolVal(num_two == target))
    if solver.check() == sat:
        found_options.append(letter)

if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")