from z3 import *

solver = Solver()

# Declare variables for each cargo type
f = Int('fuel')
g = Int('grain')
l = Int('livestock')
m = Int('machinery')
p = Int('produce')
t = Int('textiles')

# All variables are between 1 and 6 inclusive
solver.add(1 <= f, f <= 6)
solver.add(1 <= g, g <= 6)
solver.add(1 <= l, l <= 6)
solver.add(1 <= m, m <= 6)
solver.add(1 <= p, p <= 6)
solver.add(1 <= t, t <= 6)

# All distinct
solver.add(Distinct([f, g, l, m, p, t]))

# Constraints from problem
solver.add(g > l)          # grain higher than livestock
solver.add(l > t)          # livestock higher than textiles
solver.add(p > f)          # produce higher than fuel
solver.add(Or(p == t + 1, p == t - 1))  # textiles next to produce (adjacent)

# Base constraints are now added

# Test each option
found_options = []
options = [
    ("A", l == 1),
    ("B", l == 2),
    ("C", l == 3),
    ("D", l == 5),
    ("E", l == 6)
]

for letter, constr in options:
    solver.push()
    solver.add(constr)
    if solver.check() == sat:
        found_options.append(letter)
    solver.pop()

# Output according to skeleton
if len(found_options) == 1:
    print("STATUS: sat")
    print(f"answer:{found_options[0]}")
elif len(found_options) > 1:
    print("STATUS: unsat")
    print(f"Refine: Multiple options found {found_options}")
else:
    print("STATUS: unsat")
    print("Refine: No options found")