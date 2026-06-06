from z3 import *

solver = Solver()

# Create integer variables for each clue, representing chapter number (1-7)
clues = ['R', 'S', 'T', 'U', 'W', 'X', 'Z']
vars = {c: Int(f'pos_{c}') for c in clues}

# Each chapter 1-7 is used exactly once (all different)
solver.add(Distinct([vars[c] for c in clues]))

# Domain: each clue is in chapter 1-7
for c in clues:
    solver.add(vars[c] >= 1)
    solver.add(vars[c] <= 7)

# Constraint 1: T cannot be mentioned in chapter 1
solver.add(vars['T'] != 1)

# Constraint 2: T must be before W, exactly two chapters separating them
solver.add(vars['T'] < vars['W'])
solver.add(vars['W'] - vars['T'] == 3)

# Constraint 3: S and Z cannot be adjacent
solver.add(Abs(vars['S'] - vars['Z']) != 1)

# Constraint 4: W and X cannot be adjacent
solver.add(Abs(vars['W'] - vars['X']) != 1)

# Constraint 5: U and X must be adjacent
solver.add(Abs(vars['U'] - vars['X']) == 1)

# Now evaluate each option

found_options = []

# Option A: R is mentioned in chapter 7
solver.push()
solver.add(vars['R'] == 7)
if solver.check() == sat:
    found_options.append('A')
solver.pop()

# Option B: T is mentioned in chapter 5
solver.push()
solver.add(vars['T'] == 5)
if solver.check() == sat:
    found_options.append('B')
solver.pop()

# Option C: U is mentioned in chapter 7
solver.push()
solver.add(vars['U'] == 7)
if solver.check() == sat:
    found_options.append('C')
solver.pop()

# Option D: W is mentioned in chapter 3
solver.push()
solver.add(vars['W'] == 3)
if solver.check() == sat:
    found_options.append('D')
solver.pop()

# Option E: X is mentioned in chapter 6
solver.push()
solver.add(vars['X'] == 6)
if solver.check() == sat:
    found_options.append('E')
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