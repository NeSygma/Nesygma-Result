from z3 import *

solver = Solver()

# Declare the positions (1 to 6)
positions = [Int(f'pos_{i}') for i in range(6)]

# Declare the singers
singers = ['Kammer', 'Lugo', 'Trillo', 'Waite', 'Yoshida', 'Zinn']
singer_vars = {s: Int(s) for s in singers}

# Each position has exactly one singer
for i in range(6):
    solver.add(And([positions[i] == singer_vars[s] for s in singers]))
    solver.add(Distinct(positions))

# Each singer is assigned to exactly one position
for s in singers:
    solver.add(Or([singer_vars[s] == positions[i] for i in range(6)]))

# Kammer's and Lugo's auditions are recorded; others are not
recorded = [singer_vars['Kammer'], singer_vars['Lugo']]
not_recorded = [s for s in singers if s not in ['Kammer', 'Lugo']]

# The fourth audition cannot be recorded
solver.add(Not(Or([positions[3] == r for r in recorded])))

# The fifth audition must be recorded
solver.add(Or([positions[4] == r for r in recorded]))

# Waite's audition must take place earlier than the two recorded auditions
waite_pos = singer_vars['Waite']
for r in recorded:
    solver.add(Or([
        And(waite_pos == positions[i], 
            Or([r == positions[j] for j in range(i+1, 6)]))
        for i in range(5)
    ]))

# Kammer's audition must take place earlier than Trillo's audition
solver.add(Or([
    And(singer_vars['Kammer'] == positions[i], 
        Or([singer_vars['Trillo'] == positions[j] for j in range(i+1, 6)]))
    for i in range(5)
]))

# Zinn's audition must take place earlier than Yoshida's audition
solver.add(Or([
    And(singer_vars['Zinn'] == positions[i], 
        Or([singer_vars['Yoshida'] == positions[j] for j in range(i+1, 6)]))
    for i in range(5)
]))

# Additional constraint: Kammer's audition is immediately before Yoshida's
solver.add(Or([
    And(singer_vars['Kammer'] == positions[i], 
        singer_vars['Yoshida'] == positions[i+1])
    for i in range(5)
]))

# Base constraints are set. Now evaluate the multiple-choice options.

# Define the options as constraints
opt_A = (singer_vars['Kammer'] == positions[1])  # Kammer's audition is second
opt_B = (singer_vars['Trillo'] == positions[3])   # Trillo's audition is fourth
opt_C = (singer_vars['Waite'] == positions[2])   # Waite's audition is third
opt_D = (singer_vars['Yoshida'] == positions[5])  # Yoshida's audition is sixth
opt_E = (singer_vars['Zinn'] == positions[1])     # Zinn's audition is second

# Evaluate each option
found_options = []
for letter, constr in [("A", opt_A), ("B", opt_B), ("C", opt_C), ("D", opt_D), ("E", opt_E)]:
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